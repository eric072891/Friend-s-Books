# Friend-s-Books
This is a simple 4 day project to learn some SQl (Barely). I ended up learning more about setting up MySQL, APIs, and adding users with certain permissions
and creating tables. 
The code intent is as follows. My friend has a list of books he wants to read in the future. This list is compiled on the Goodreads website. 
Unfortunately, the books on this website don't have tags. They aren't sorted by category: fiction, romance, history, etc. 
However, google books does sort their books by category. 
I use R as my programming language. First, I download the metadata of my friend's books from Goodreads using their API.
Then, I search for the corresponding title using the Google Books API. I download the JSON file and use string manipulation to get the relevant information. 
Each book has its title, ISBN13, page count, maturity rating, and category stored as a row of a data frame. 
Then, using the RMariaDatabase package for R, I transfer the information in the data frame into a SQL table in the MySQL server I've created. 

TODO: create a simple website for my friend to search his books by category
