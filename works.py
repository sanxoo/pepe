from fastapi import APIRouter

import broker

router = APIRouter()


@router.get("/works/{name}", status_code=202)
async def get(name: str):
    await broker.work_hard.kiq(name)
