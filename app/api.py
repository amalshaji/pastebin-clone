import uuid

from fastapi import APIRouter, HTTPException, status

from app.database import database, paste
from app.schemas import AddPaste, GetPaste

from passlib.hash import bcrypt

api = APIRouter(prefix="/api")


def generate_uid() -> str:
    return uuid.uuid4().hex[:6]


@api.post("/get")
async def retrieve_paste(req: GetPaste):
    query = paste.select().where(paste.c.id == req.id)
    res = await database.fetch_one(query)
    if res is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="invalid id",
        )
    if res.password_hash is not None:
        if req.password == "" or req.password is None:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Password required",
            )
        if bcrypt.verify(req.password, res.password_hash):
            return res.text
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Wrong password",
            )
    return res.text


@api.post("/")
async def add_paste(req: AddPaste):
    id = generate_uid()
    if req.password:
        req.password = bcrypt.hash(req.password)
        query = paste.insert().values(
            id=id,
            text=req.text,
            password_hash=req.password,
        )
    else:
        query = paste.insert().values(
            id=id,
            text=req.text,
        )
    _ = await database.execute(query)
    return id
