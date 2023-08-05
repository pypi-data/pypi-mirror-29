Peach Runner
============

This test runner will send requests via Peach API Security to perform testing
of a target api.  There are several methods for sending requests:

  - Burp file with recorded requests. Each request is tested one at a time.
  - Postman collection with requests. Each request is tested one at a time.
  - Single command line (ex: curl, python script, etc.)
  - Text file with one-command per line
  - Directory with executable scripts/programs, each executed in sequence


Installation
------------

Install required python dependencies with internet connection.

$ pip install -r requirements.txt

Offline Installation
--------------------

Install required python dependencies using our offline dependencies
folder.

$ pip install --no-index --find-links ../../deps -r requirements.txt
