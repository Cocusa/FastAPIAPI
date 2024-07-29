__version__ = '1.0'

import platform

from fastapi import Depends, FastAPI, Query, Request, Path

from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

import fdb

from .dependencies import get_db
from .routers import bom
from .routers import device_card
from .routers import csv_reports
from .routers.v1 import files as files_v1

if any(platform.win32_ver()):
    fdb.load_api("./fbclient.dll")

description = """
API

"""

tags_metadata = [
    {
        "name": "bom",
        "description": "Спецификации",
    },   
    {
        "name": "employees",
        "description": "Пользователи",
    },
    {
        "name": "csv_reports",
        "description": "Выгрузка отчетов",
    },
]

app = FastAPI(
    title="123",
    version="1.0.0",
    description=description,
    contact={
        "name": "123",
        "email": "123@123",
    },
    openapi_tags=tags_metadata
)

app.include_router(bom.router)
app.include_router(device_card.router)
app.include_router(csv_reports.router)

@app.exception_handler(fdb.fbcore.DatabaseError)
async def fdb_exception_handler(_: Request, exc: fdb.fbcore.DatabaseError):
    """Глобальный обработчик исключений БД
    """
    return JSONResponse(
        status_code=500,
        content={"message": str(exc)},
    )

origins = [
    "http://localhost:4200", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)




