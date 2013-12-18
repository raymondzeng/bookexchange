bookexchange
============

Everything here is up for discussion

## General Structure:

The main focus is **UX**. Has to be very **easy to use**. but of course functionality is important too

* a *post* is an instance of someone selling some book; 
  * In the database, the following should be **stored**:
    * something to link it to the seller
    * the book being sold
    * the condition of the book
    * the price wanted
    * the date the post was submitted
  * On a book's page, each post should **show**
    * the condition
    * date submitted
    * price info
    * way of contacting seller
   
* Home page
  * if user is **not** logged in, show a login panel, some text describing thebookexchange, and perhaps a carousel with the most recent *posts*
  * if user is logged in, show a list of their pending *posts*, i.e. books they are trying to sell, and some panel relating to the books they are *subscribed* to(refer to TODO)
* Search
  * Users do not need to be signed in or registered to search
  * the search results will display a list of books that match the search query; every book in this results list should be unique
  * when a user clicks on a link in the search results page, they go to that book's page; every book has it's own page
  * on this page, the top section will have general info about the book, title author, amazon link, picture, etc
  * on the bottom will be a list of *posts* that are trying to sell this book and this list can be sorted by price, date
  * from here, our job is done and the user contacts the seller to negotiate amongst themselves
* Selling
  * must be logged in
  * first enter the ISBN of the book, ajax load the info of the book so they know they entered the correct ISBN
  * next enter condition and price (we need some way to differentiate if price is definite, lowest, a range, negotiable etc)
  * enter a way to contact seller, phone number, facebook, email etc. This can be saved in the user's account so it doesn't have to be entered every time
  * users are responsible for deleting a post after a sell or if no longer valid so *deleting posts should be easy*
  
## TODO:

### Critical
* login/account system:
  * users will register with an account name, password, and their email
  * store preferred contact method
  * LATER FEATURE: option to sign in with facebook/google
* Searching/submitting *posts*
  * store posts in a way that its easy to quickly get all the posts selling the same book
  * store data so Searching as outlined in General Structure is fast and accurate
  * general and advanced search

### Not so critical
* Subscribing
  * users can 'follow' a book so they get an email everytime someone submits a *post* selling that book

* Get all the books that Brown Courses use so we have a good set of books to begin with 