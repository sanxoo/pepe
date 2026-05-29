from fastapi import FastAPI, Security, Depends, UploadFile, Response, HTTPException
from fastapi.security import APIKeyHeader
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from aiopath import AsyncPath
from contextlib import asynccontextmanager

import logging
import dotenv
import os

import db
import users
import works

dotenv.load_dotenv()

_api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)
_api_key = os.getenv("API_KEY")


async def validate_api_key(api_key: str = Security(_api_key_header)):
    if _api_key != api_key:
        raise HTTPException(401, detail="unauthorized")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect()
    yield
    await db.disconn()


app = FastAPI(
    dependencies=[Depends(validate_api_key)],
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"]
)


@app.get("/api/v1/files")
async def ls():
    res = []
    async for path in AsyncPath("files").iterdir():
        if await path.is_file():
            res.append(path.name)
    return res


@app.post("/api/v1/files", status_code=200)
async def upload(file: UploadFile, response: Response):
    content = await file.read()
    path = AsyncPath(f"files/{file.filename}")
    if not await path.exists():
        response.status_code = 201
    size = await path.write_bytes(content)
    logging.debug("write %s bytes to %s", size, path)
    return {}


@app.get("/api/v1/files/{name}", response_class=FileResponse)
async def download(name: str):
    path = AsyncPath(f"files/{name}")
    if not await path.exists():
        raise HTTPException(404, detail="file not found")
    return FileResponse(path, filename=name)


@app.delete("/api/v1/files/{name}", status_code=204)
async def remove(name: str):
    path = AsyncPath(f"files/{name}")
    if not await path.exists():
        raise HTTPException(404, detail="file not found")
    await path.unlink()
    return None


app.include_router(users.router, prefix="/api/v1")
app.include_router(works.router, prefix="/api/v1")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, log_config="log.json")
