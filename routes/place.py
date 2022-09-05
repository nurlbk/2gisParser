from fastapi import APIRouter, FastAPI

from models.place import Place
from config.db import conn
from twogisParser import parseFirst, parseAll

placeApi = APIRouter()


@placeApi.get("/search/{item_name}")
async def get_place(item_name: str):
    return dict(parseFirst("https://2gis.kz/nur_sultan", item_name))


@placeApi.post("/search/{item_name}")
async def create_place(item_name: str):
    place = parseFirst("https://2gis.kz/nur_sultan", item_name)
    try:
        conn.local.places.insert_one(dict(place))
    except:
        pass
    return dict(place)


@placeApi.get("/category/{category_name}")
async def get_category(category_name: str):
    return dict(parseAll("https://2gis.kz/nur_sultan", category_name))


@placeApi.post("/category/{category_name}")
async def create_category(category_name: str):
    places = parseAll("https://2gis.kz/nur_sultan", category_name)
    try:
        conn.local.categories.insert_one(dict(places))
    except:
        pass
    return dict(places)
