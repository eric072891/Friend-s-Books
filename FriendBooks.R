#Eric Olberding 6/25/2020
#Goodreads is a website where people can create lists of books they have read or want to buy, among other things
#Unfortunately, Goodreads does not classify its books by subject or style
#The goal of this code is to take my friend's Goodreads want-to-read books and obtain the titles and isbn using the Goodreads
#api. This information is then used to find the subject of the book using the Google Books api.
#To practice sql, I create a sql database with book title, isbn13 number, page count, maturity rating, and subject.

#goodreads api key: 0Fqoo6dizYhNM8OeCgHpw
#secret: cozXtdxYqKylqkvE5LpqgiZ04vkYCzIaOhXYVCcDgM

library(httr)
library(jsonlite)
library(XML)
library(stringr)
library(purrr)
library(RMariaDB)

#First, we get data on books in Friend's Goodreads Shelf via the Goodreads API
#could make this more general by first parsing initial response for number of books
#then iterating over an integer determined over this total number
#but I'm probably never goingt to do this specific thing again
res.1 = GET('https://www.goodreads.com/review/list/.xml?key=0Fqoo6dizYhNM8OeCgHpw&v=2&shelf=want-to-read&per_page=200&page=1')
res.2 = GET('https://www.goodreads.com/review/list/.xml?key=0Fqoo6dizYhNM8OeCgHpw&v=2&shelf=want-to-read&per_page=200&page=2')
res.3 = GET('https://www.goodreads.com/review/list/.xml?key=0Fqoo6dizYhNM8OeCgHpw&v=2&shelf=want-to-read&per_page=200&page=3')
res.4 = GET('https://www.goodreads.com/review/list/.xml?key=0Fqoo6dizYhNM8OeCgHpw&v=2&shelf=want-to-read&per_page=200&page=4')
res.5 = GET('https://www.goodreads.com/review/list/.xml?key=0Fqoo6dizYhNM8OeCgHpw&v=2&shelf=want-to-read&per_page=200&page=5')

#Books on Friends Goods Reads Shelf in single character vector, split into char vec
#for each book
Friend.data1 = str_split(rawToChar(res.1$content),"\n</review>\n\n    <review>\n")
Friend.data2 = str_split(rawToChar(res.2$content),"\n</review>\n\n    <review>\n")
Friend.data3 = str_split(rawToChar(res.3$content),"\n</review>\n\n    <review>\n")
Friend.data4 = str_split(rawToChar(res.4$content),"\n</review>\n\n    <review>\n")
Friend.data5 = str_split(rawToChar(res.5$content),"\n</review>\n\n    <review>\n")
dat.list = c(Friend.data1,Friend.data2,Friend.data3,Friend.data4,Friend.data5)
Friend.data = do.call(c,dat.list)
rm(Friend.data1,Friend.data2,Friend.data3,Friend.data4,Friend.data5, dat.list)

#find isbn and title of each book

isbn13s = lapply(Friend.data, function(x) str_extract(str_extract(x, regex("<isbn13>\\d{13}</isbn13>")), regex("\\d{13}")))
titles = lapply(Friend.data, function(x) str_replace_all(str_extract(x, regex("<title>.*</title>")), regex("<.*?>"),""))

#turn them from lists into vectors
isbn13s = unlist(isbn13s)
titles = unlist(titles)

#new data frame containing all properties (eventually)
Friend.books = data.frame(isbn.13 = isbn13s,
                         title = titles)

#convert variables from factor variables to character variables
Friend.books$isbn.13=as.character(Friend.books$isbn.13)
Friend.books$title=as.character(Friend.books$title)

#############
#############
#Next we use the ISBNs and Titles to query Googles API about the books category, number of pages
#and maturity level
#############

#metadata for a book obtained from google api
page.count = character()
category = character()
maturity.rating = character()

for(i in 1:nrow(Friend.books)){
  metadata = GET(paste('https://www.googleapis.com/books/v1/volumes?q=intitle:',str_replace_all(Friend.books[i,2],' ','+'),'+isbn:',Friend.books[i,1], sep = ''))
  
  content = rawToChar(metadata$content)
  category[i] = str_replace_all(str_extract(content, regex('categories\".*?\\n.*?\\\"\\n', dotall=TRUE)), c('categories\": \\[\n.*?\"' = '','\\\"\\n'= ''))
  maturity.rating[i] = str_replace_all(str_extract(content, regex('maturityRating\".*?,', dotall=TRUE)), c('maturityRating\": \"' = '','\",'= ''))
  page.count[i] = str_replace_all(str_extract(content, regex('pageCount\\\":.*?,', dotall=TRUE)), c('pageCount\\\": ' = '',','= ''))
}

Friend.books$page.count = page.count
Friend.books$maturity.rating = maturity.rating
Friend.books$category = category



#a little data cleaning, redundant categories, could have forced into lower case
unique(Friend.books$category)
Friend.books$category[which(Friend.books$category=='FICTION')] = 'Fiction'
Friend.books$category[which(Friend.books$category=='FAMILY & RELATIONSHIPS')] = 'Family & Relationships'
Friend.books$category[which(Friend.books$category=='HISTORY')] = 'History'
unique(Friend.books$category)

#check which books only have titles and remove them
remove.books = function(x){
  if(is.na(Friend.books$isbn.13[x]) & is.na(Friend.books$page.count[x]) & 
     is.na(Friend.books$maturity.rating[x]) & is.na(Friend.books$category[x])){
    FALSE 
  }
  else{
    TRUE
  }
}
keep.rows = unlist(lapply(1:nrow(Friend.books), remove.books))

Friend.books = Friend.books[keep.rows,]
Friend.books = Friend.books[!duplicated(Friend.books$title),]
#####################################
###SQL section
#####################################

#Use RMariaDB to interface with mysql server and add data frame information to table Friends_books
#User: booksuser has access to the table and can edit it

editor.password = "meh"

#query function: it creates a query for the xth row in the data.frame Friend.books
insert.data = function(x){
  query = paste('INSERT INTO books (
title,
isbn13,
pageCount,
maturityRating,
category)
VALUES(\'', str_replace_all(Friend.books$title[x],"\'", "\'\'"),"\',\'",Friend.books$isbn.13[x],"\',\'",
                Friend.books$page.count[x], "\',\'", Friend.books$maturity.rating[x], "\',\'", str_replace_all(Friend.books$category[x],"\'","\'\'"), "\');", sep = '')
  
  booksInsert <- dbSendQuery(booksDb, query)
  dbClearResult(booksInsert)
}


#connect to database
booksDb <- dbConnect(RMariaDB::MariaDB(), user='booksuser', password=editor.password, dbname='Friends_books', host='localhost')

#inserts information into the table
lapply(1:nrow(Friend.books), insert.data)

#disconnects from database
dbDisconnect(booksDb)
