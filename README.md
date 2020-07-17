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

Next, using Django, we develop a webpage for my friend to see his books in each category. The homepage is a sorted list of categories his books fall in. Each category is a clickable link that takes you to the set of books in that category. 

TODO: host the database and web framework Django files on a webserver (digital ocean, heroku, or something). Also, potentially rewrite the python code to do what the R code does (API query and string regex) to have it in one place. Then, any good reads user could find category tags associated with their books. However, this would involve more stringent cleaning of the category data from google (more users==more categories, would have be more general in the text cleaning)


Note: I've removed any identifiers of my friend so the uploaded code won't work. The GET commands at the start require a userid before ".xml" in the address.
