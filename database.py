from sqlalchemy import create_engine
from fastapi import FastAPI
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2

app = FastAPI()

DATABASE_URL = "postgresql://postgres:1234@localhost:5432/fastapi"

engine = create_engine(DATABASE_URL,)

Base = declarative_base()

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


async def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.on_event("startup")
async def startup():
    app.db_connection = psycopg2.connect(DATABASE_URL)


@app.on_event("shutdown")
async def shutdown():
    app.db_connection.close()
