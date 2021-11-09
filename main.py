"""
Integration with FastAPI.
=========================

To test, first, start the server:

    $ uvicorn --reload main:test

Then, in another shell, create a user:

    $ curl -X POST -H 'Content-Length: 0' "http://localhost:8000/user"
    {"pk":"01FM11YW3ZXH6XZHEWTAJHFNC7","first_name":"Andrew","last_name":"Brookins","email":"andrew.brookins@example.com","join_date":"2021-11-08","age":38,"bio":"Python developer, works at
    Redis, Inc."}

Get a copy of the value for "pk" and make another request to get that user:

    $ curl "http://localhost:8000/user/01FM11YW3ZXH6XZHEWTAJHFNC7"
    {"pk":"01FM11YW3ZXH6XZHEWTAJHFNC7","first_name":"Andrew","last_name":"Brookins","email":"andrew.brookins@example.com","join_date":"2021-11-08","age":38,"bio":"Python developer, works at
Redis, Inc."}

You can also get a list of all user PKs:

    $ curl "http://localhost:8000/users"
    {"users":["01FM11YW3ZXH6XZHEWTAJHFNC7"]}
"""

import datetime
from typing import Optional

import aioredis

from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from fastapi_cache.decorator import cache

from pydantic import EmailStr

from redis_om.model import HashModel


class Customer(HashModel):
    first_name: str
    last_name: str
    email: EmailStr
    join_date: datetime.date
    age: int
    bio: Optional[str]


app = FastAPI()


@app.post("/user")
async def save_user():
    # First, we create a new `Customer` object:
    user = Customer(
        first_name="Andrew",
        last_name="Brookins",
        email="andrew.brookins@example.com",
        join_date=datetime.date.today(),
        age=38,
        bio="Python developer, works at Redis, Inc."
    )

    # We can save the model to Redis by calling `save()`:
    user.save()

    return user.dict()


@app.get("/users")
async def list_users(request: Request, response: Response):
    # To retrieve this customer with its primary key, we use `Customer.get()`:
    return {"users": Customer.all_pks()}


@app.get("/user/{pk}")
@cache(expire=10)
async def get_user(pk: str, request: Request, response: Response):
    # To retrieve this customer with its primary key, we use `Customer.get()`:
    return Customer.get(pk).dict()


@app.on_event("startup")
async def startup():
    r =  aioredis.from_url("redis://localhost:6381", encoding="utf8", decode_responses=True)
    FastAPICache.init(RedisBackend(r), prefix="fastapi-cache")
