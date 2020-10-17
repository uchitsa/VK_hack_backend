from typing import List
from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise, HTTPNotFoundError
import crud
import schemas
from models import (
    User, UserPydantic, UserInPydantic, UserPydanticList,
    City, CityPydantic, CityPydanticList,
    Region, RegionPydantic, RegionPydanticList,
    Category, CategoryPydantic, CategoryPydanticList,
)
from vkwave.api import API
from vkwave.client import AIOHTTPClient
import json


vk_api_session = API(
    tokens='1c868585d7c67dc159152ef3ec48c69250ce9dad75fd0c8d2d05a9e42b6ac67bc028097934ecdd58c9e4a',
    clients=AIOHTTPClient()
)

vk_api = vk_api_session.get_context()
app = FastAPI()


def get_json(x) -> dict:
    return json.loads(x.json())


def get_json_items(x) -> List:
    return get_json(x)['response']['items']


@app.get("/categories")
async def get_categories():
    return await CategoryPydantic.from_queryset(Category.all())


@app.get("/region")
async def get_regions():
    return await RegionPydantic.from_queryset(Region.all())


@app.get("/region/{region_id}")
async def get_regions(region_id: int):
    region = await Region.get(id=region_id)
    return await CityPydantic.from_queryset(City.filter(region__istartswith=region.title))


@app.get("/city")
async def get_cities():
    return await CityPydantic.from_queryset(City.all())


@app.get("/init", response_model=schemas.Status, responses={404: {"model": HTTPNotFoundError}})
async def init_db():
    message = ''
    if await Region.first() is None:
        for region in get_json_items(await vk_api.database.get_regions(country_id=1, count=1000)):
            await Region.create(
                id=region['id'],
                title=region['title']
            )
            cities = get_json_items(await vk_api.database.get_cities(
                country_id=1, region_id=region['id'], need_all=True, count=1000))
            for city in cities:
                await City.create(
                    id=city['id'],
                    title=city['title'],
                    area=city['area'],
                    region=city['region']
                )
        message += '[INFO] Данные о Городах занесены в БД\n'
    return schemas.Status(message=message)


register_tortoise(
    app,
    db_url="sqlite://sql_app.db",
    modules={"models": ["models"], "aerich.models": ["models"]},
    generate_schemas=True,
    add_exception_handlers=True,
)
