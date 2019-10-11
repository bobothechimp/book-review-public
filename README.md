# Project 1

Web Programming with Python and JavaScript

My project is (of course) a book reviewing website called "Book Talks". People can create accounts, log into those accounts, search through the catalog of 5000 books, and leave reviews for those books. They can even use the API by following the "/api/<isbn>" path in the URL.



FILE DIRECTORIES:

All html files can be found under the "templates" folder. This includes:
  - layout.html, the layout for all pages
  - index.html, the home page
  - signup.html, the sign up page
  - registered.html, the page telling users they've signed up
  - login.html, the log in page
  - loggedin.html, the page telling users they've logged in
  - logout.html, the page telling users they've logged out
  - catalog.html, the catalog page
  - catalogBook.html, the page displaying information about a certain book


All files related to css can be found under the "css" folder.

All files related to SQL, databases, and table creation can be found under the "sql" folder.
  - accounts.sql, the information of all registered accounts
  - books.sql, the information of all 5000 books
  - reviews.sql, the information of all reviews of all books

The provided "books.csv" file as well as the required "import.py" file can be found under the "importing" folder.


DATABASE TABLES:

"accounts"
  "username", a text column to store an account's username
  "password", a text column to store an account's (hashed) password
  "user_id", a serial key to represent the id of a certain account

"books"
  "title", a text column representing the title of the book
  "author", a text column representing the author of the book
  "year", an integer column representing the year the book was published
  "isbn", a text column representing the book's ISBN

"reviews"
  "poster", a text column representing the username of the person who posted the review
  "review_text", a text column representing the actual review itself
  "isbn", a text column representing the isbn of the book the review is for



EXTRA NOTES:

For some reason the font size and padding of some classes (.toplinks, .desc, etc.) would not change when a font size or padding size was specified in the stylesheet, so I had to include the styling inside the head of "layout.html"

I'm sorry if some parts of the website don't look great visually; I was in a bit of a rush to finish the project after I had lots of trouble with the setup and installing everything.



SOURCES:

Hashcode encrypting and verification functions: https://www.vitoshacademy.com/hashing-passwords-in-python/
                                                https://pythonprogramming.net/password-hashing-flask-tutorial/
If-statement to check if a sequence is empty: https://stackoverflow.com/questions/53513/how-do-i-check-if-a-list-is-empty
Documentation for bootstrap list group component: https://getbootstrap.com/docs/4.3/components/list-group/
Documentation for bootstrap form component: https://getbootstrap.com/docs/4.3/components/forms/
