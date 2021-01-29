from fastapi import FastAPI

from app.api import api
from app.database import database

app = FastAPI()
app.include_router(api)


@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()