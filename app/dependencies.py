from os import getenv

import fdb

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()


def get_db(credentials: HTTPBasicCredentials = Depends(security)) -> fdb.Connection:
    try:
        dbcon = fdb.connect(
            getenv('DSN'),
            credentials.username,
            credentials.password,
            charset='utf-8',
            role='123'
        )
    except fdb.DatabaseError as db_err:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        ) from db_err
    try:
        yield dbcon
        dbcon.commit()
    finally:
        dbcon.close()