from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from psycopg2.extras import RealDictCursor

import db


class User(BaseModel):
    mail: str
    name: str


router = APIRouter()


@router.post("/users")
async def insert(user: User):
    async with db.pool.acquire() as conn:
        async with conn.cursor() as curs:
            query = "INSERT INTO users VALUES ( %(mail)s, %(name)s ) ON CONFLICT (mail) DO UPDATE SET name = %(name)s "
            await curs.execute(query, user.model_dump())
            return user


@router.get("/users/{mail}", response_model=User)
async def get(mail: str):
    async with db.pool.acquire() as conn:
        async with conn.cursor(cursor_factory=RealDictCursor) as curs:
            query = "SELECT mail, name FROM users WHERE mail = %s "
            await curs.execute(query, (mail,))
            user = await curs.fetchone()
            if not user:
                raise HTTPException(404, detail="user not found")
            return user


@router.delete("/users/{mail}", status_code=204)
async def delete(mail: str):
    async with db.pool.acquire() as conn:
        async with conn.cursor() as curs:
            query = "DELETE FROM users WHERE mail = %s "
            await curs.execute(query, (mail,))
            return None
