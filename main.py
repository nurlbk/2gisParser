from fastapi import FastAPI
from routes.place import placeApi
from twogisParser import parseFirst, parseAll

app = FastAPI()
app.include_router(placeApi)


