A server that exposes an HTTP-based API that is designed to receive a string of URL-encoded characters that can be used by the caller to determine whether the string is a duplicate, i.e. has already been seen by the server.

The HTTP server implements the following 2 API functions:

Submit a string for deduplication
Request:
POST /sequence/{sequence}
Response codes:
200 Description: Message received
Response body: {“duplicate”: [true|false]}

Clear deduplication history
Request:
PUT /clear
Response codes:
200 Description: Deduplication history cleared

== Installation ==
Wants a modern Python (tested on 3.9)
Clone this repo
git clone https://github.com/flavour/im
Setup a venv:
python -m venv venv_im
source venv_im/bin/activate
pip install -r im/requirements.txt

== Run ==
cd im
uvicorn main:app

You can view/test the API via:
http://127.0.0.1:8000/docs

== Productionise ==
* Add Authentication
* Switch to a DB like Postgres
* Front uivcorn with nginx and gunicorn -w 4 -k uvicorn.workers.UvicornWorker
* Try to get modified version of framework components integrated upstream
