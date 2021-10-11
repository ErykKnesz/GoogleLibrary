# GoogleLibrary

## About this app
This is a little library app built to store data about books added manually or from Google API. Other Features include:
* editing books,
* filtering (exact match) with keywords matching database fields,
* searching as above but resuluting output contains all similar entries.

The app can be used as a web app with forms powered by Flask WTForms or by API (API currently only for data reading, no editing or deleting supported as of yet).
The front-end was built using Bootstrap 4.6.0. The back-end mostly consists of Flask, Flask-SQLAlchemy, Flask-WTForms, a comprehensive list of requirements is uploaded.
The Library data is stored in SQLite Database.

## How to run on a development server

1. Clone the repo.
2. Define your env. variables `SECRET_KEY` and optionally `FLASK_APP`
3. `flask run` if you defined FLASK_APP variable or `python library.py` to run the development server.

The app comes with a sample databe library.db. - can be removed but then `flask db upgrade` should be run to create a new one.

Deployed on Heroku (https://eryk-library.herokuapp.com/)
