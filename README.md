# Simple Flask API

This is a simple project meant to showcase implementing a small API. Thanks for reviewing!

## Description

The system maintains a record of all POSTed values to /metric/<metric_name> for an hour and returns the sum on GET to /metric/<metric_name>/sum. The majority of the work is done in cache.py, where we're utilizing an in-memory global cache variable as opposed to a db for simplicity.

## Getting Started

### Dependencies

* python 3.6+
* See requirements.txt

### Executing program

* Setup/activate venv virtual environment
* pip install -r requirements.txt
* export FLASK_APP=flask_api
* flask run

## Authors

Contributors names and contact info

ex. Dan Dimond
