import databases

import sqlalchemy
from sqlalchemy import Column, String

DB_URI = "sqlite:///./test.db"

database = databases.Database(DB_URI)

metadata = sqlalchemy.MetaData()

paste = sqlalchemy.Table(
    "paste",
    metadata,
    Column("id", String, primary_key=True),
    Column("text", String, nullable=False),
    Column("password_hash", String, nullable=True),
)

engine = sqlalchemy.create_engine(
    DB_URI,
    connect_args={"check_same_thread": False},
)

metadata.create_all(engine)