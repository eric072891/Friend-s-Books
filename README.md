# Friend-s-Books
This is a simple 10 day project to practice SQL and Python. I ended up learning more about setting up MySQL, APIs, and adding users with certain permissions
and creating tables. 
The code intent is as follows. My friend has a list of books he wants to read in the future. This list is compiled on the Goodreads website. 
Unfortunately, the books on this website don't have tags. They aren't sorted by category: fiction, romance, history, etc. 
However, google books does sort their books by category. 
Using R, I download the metadata of my friend's books from Goodreads using their API.
Then, I search for the corresponding title using the Google Books API. I download the JSON file and use string manipulation to get the relevant information. 
Each book has its title, ISBN13, page count, maturity rating, and category stored as a row of a data frame. 
Then, using the RMariaDatabase package for R, I transfer the information in the data frame into a SQL table in the MySQL server I've created.

Next, using Django, we develop a webpage for my friend to see his books in each category. The homepage is a sorted list of categories his books fall in. Each category is a clickable link that takes you to the set of books in that category. 

TODO: Clean the categories that are queries from Goodreads data. Make it so that the program remembers if a user's books have already been stored. Add a CSS style sheet.


Note: I've removed any identifiers of my friend so the uploaded code won't work. The GET commands at the start require a userid before ".xml" in the address.
