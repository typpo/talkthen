talkthen
========

## Setup

  1. Install virtualenv
  
  `sudo apt-get install python-virtualenv` or `pip install virtualenv` for Macs
  
  2. Create your venv in the source root:
  
  `virtualenv venv`
  
  3. Activate it (this must be done whenever you want to run the app):
  
  source venv/bin/activate
  
  4. Install project dependencies
  
  `pip install -r requirements.txt`
  
  5. cd into the app and start the development server
  
  `cd talkthen`
  `./manage.py runserver 0.0.0.0:3333`
  
  In your browser: http://localhost:3333

## Organization

`api/` - uses django rest framework to provide an API for PhoneNumbers and Calls.  In the beginning I wanted to do everything through this.  This is not strictly necessary and I've been violating the RESTiness of everything by putting logic in `core/views.py`.

`core/` - all the telephony stuff.  See `views.py` and `conference.py`

`web/` - the web view (just one page now)
