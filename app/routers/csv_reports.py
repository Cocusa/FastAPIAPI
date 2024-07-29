import csv
from datetime import date
from io import StringIO
from typing import Any, Iterable
from fastapi import APIRouter, Depends, Query
from fastapi.responses import StreamingResponse

import fdb

from app.dependencies import get_db

router = APIRouter()


def make_csv(header: Iterable[Any], data: Iterable[Any]) -> str:
    with StringIO() as stream:
        writer = csv.writer(stream)

        writer.writerow(header)
        writer.writerows(data)

        return stream.getvalue()


@router.get('/api/csv_reports/123',
            summary='Выгрузка статистики маршуртов за заданный период',
            tags=["csv_reports"])
def get_route_statistics_test(date_start: date | None = Query(title='Дата начала поиска в формате yyyy-MM-dd',
                                                              default=None),
                              date_end: date | None = Query(title='Дата окончания поиска в формате yyyy-MM-dd',
                                                            default=None),
                              dbcon: fdb.Connection = Depends(get_db)):
    sql_cmd = 'select 123 from 123(?,?)'
    cursor = dbcon.cursor().execute(sql_cmd, (date_start, date_end,))

    return StreamingResponse(
        iter([make_csv([item[0] for item in cursor.description], cursor.fetchall())]),
        media_type="text/csv", headers={"Content-Disposition": "attachment; filename=route_statistics.csv"})
