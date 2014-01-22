talkthen
========

# Setup

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
