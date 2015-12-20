Requirements

-An endpoint that receives a URL and returns a new shortened URL
   -Checks if URL exists in Short_URLs.short_url's or Custom_URLs.custom_url's
   -if it does, updates existing Short_URL object's timestamp, and returns the existing shortened URL
   -if it does not exist, creates a new Short_URL object, saves it with django orm

-An endpoint to retrieve the last 100 shortened URLs
   -index db by timestamp
   -return last 100 according to that index

-An endpoint to retrieve the top 10 most popular shortened domains in the past month
   -groups urls by domain and returns total of each (for the top ten)

-An endpoint to retrieve the number of times a shortened URL has been visited.
   -Checks if url exists in Short_URLs.short_urls or Custom_URLs.custom_urls
   -If it does, note whether it exists specifically Short_URLs or Custom_URLs
      -If it exists in Custom_URLs, look up the Custom_URL's foreign key and use that to look up the number of visits in Short_URLs
      -If it exists in Short_URLs, look up the Short_URL's number_visits attribute
   -If not, return 0, indicating 0 visits

-An endpoint to support the creation of custom URLs
   -Checks if url exists in Short_URLs.short_urls or Custom_URLs.custom_urls
   -If it exists in Short_URLS, dont make Custom_URL. Return error status
   -If it exists in Custom_URLs, dont make Custom_URL. Return error status
   -If it exists in neither table, make new Custom_URL, link to Short_URL as Foreign Key 

-(My own endpoint(s)) Endpoints for visiting an shortened URL's
   -If not api endpoint, then:
      -checks if URL exists in Short_URLs or CustomURLs
      -If so, returns (or even better, goes to) shortened url's long_url
      -If not, returns message stating url does not yet exist 
   

-Utilize a relational database
   -Model: Short_URL
      -longURL (unique, primary key)
      -domain
      -short_url (unique and must not exist in Custom_URLs.custom_url's)
      -number_visits (indexed on this column)
      -last_time_stamp (another index on this column)

   -Model: Custom_URL
      -URL (Foreign-key on URL table)
      -custom_url (primary_key, must be unique and not exist in Short_URLs.short_url's)

-The URL shortener should be able to support at least 1,000,000 shortened URLs.
-Your shortened URLs should utilize no more than 6 characters (i.e. http://bit.ly/XXXXXX)
   -make random string of length 6 generator function
-Write unit tests for your code
-Comment your code appropriately
-Use Git to version control your code - we want to see your progress, so commit often.


Set up
------

$ virtualenv env
$ sudo apt-get install python-pip
$ pip install django
$ pip install djangorestframework
$ django-admin.py startproject url_shortener .
$ python manage.py runserver
   -open http://127.0.0.1:8000/ to check if django page is up

