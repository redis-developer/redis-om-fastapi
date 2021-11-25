# redis-om-fastapi

This repository contains an example of how to use [Redis OM Python](https://github.com/redis/redis-om-python) with FastAPI.

## Installing

You install this project with Poetry.

First, [install Poetry](https://python-poetry.org/docs/#installation). You can probably pip install it into your Python environment:

    $ pip install poetry

Then install the example app's dependencies:

    $ poetry install
    
## Running the Examples

This project contains two identical FastAPI applications, one synchronous (main.py) and one asynchronous (async_main.py). Both use Redis OM for Python to save and retrieve data from Redis.

To try the API, first, start the one of the servers.

You can start the synchronous server like this, from your terminal:

    $ poetry run uvicorn main:app
    
Or the async server like this:

    $ poetry run uvicorn async_main:app

Then, in another shell, create a customer:

    $ curl -X POST  "http://localhost:8000/customer" -H 'Content-Type: application/json' -d '{"first_name":"Andrew","last_name":"Brookins","email":"a@example.com","age":"38","join_date":"2020
-01-02"}'
    {"pk":"01FM2G8EP38AVMH7PMTAJ123TA","first_name":"Andrew","last_name":"Brookins","email":"a@example.com","join_date":"2020-01-02","age":38,"bio":""}

Copy the "pk" value, which is the model's primary key, and make another request to get that customer:

    $ curl "http://localhost:8000/customer/01FM2G8EP38AVMH7PMTAJ123TA"
    {"pk":"01FM2G8EP38AVMH7PMTAJ123TA","first_name":"Andrew","last_name":"Brookins","email":"a@example.com","join_date":"2020-01-02","age":38,"bio":""}

You can also get a list of all customer PKs:

    $ curl "http://localhost:8000/customers"
    {"customers":["01FM2G8EP38AVMH7PMTAJ123TA"]}
