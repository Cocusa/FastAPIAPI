from fastapi import APIRouter, Depends, Path, Query


import fdb

from ..dependencies import get_db

router = APIRouter()


@router.get('/api/bom/{bom_id}/info', summary='Информация об спецификации', tags=["bom"])
def get_bom_info(bom_id: int = Path(title='id спецификации', ge=0),
                 dbcon: fdb.Connection = Depends(get_db)):
    """Возвращает информацию об спецификации
    """
    sql_cmd = 'select BOM_LIST_ID as "id",\
                    DESCRIPT as "description",\
                from BOM_123(?)'
    return dbcon.cursor().execute(sql_cmd, (bom_id,)).fetchallmap()


@router.get('/api/bom/{bom_id}/structure', summary='Структура спецификации', tags=["bom"])
def get_bom_structure(bom_id: int = Path(title='id спецификации', ge=0),
                      dbcon: fdb.Connection = Depends(get_db)):
    """Возвращает структуру спецификации
    """
    sql_cmd = 'select BOM_ITEM_ID as "id",\
                from BOM_321(?)'
    return dbcon.cursor().execute(sql_cmd, (bom_id,)).fetchallmap()


@router.get('/api/bom/{bom_id}/tree', summary='Дерево спецификации', tags=["bom"])
def get_bom_tree(bom_id: int = Path(title='id спецификации', ge=0),
                 dbcon: fdb.Connection = Depends(get_db)):
    """Дерево составных частей спецификации
    """
    sql_cmd = 'select ID as "id"\
                from BOM_321(0, ?, 1, 0, 0, 0)'
    return dbcon.cursor().execute(sql_cmd, (bom_id,)).fetchallmap()


@router.get('/api/bom', summary='Список спецификаций',  tags=["bom"])
def get_bom_list(descript: str | None = Query(default=None,
                                              title='Описание спецификации',
                                              min_length=1,
                                              max_length=255,
                                              ),
                 str_id: int | None = Query(
        default=None, title='Участок за которым закреплена спецификация', ge=0),
        contained_bom: int | None = Query(
        default=None, title='Спецификация содрежащаяся в искомых', ge=0),
        dbcon: fdb.Connection = Depends(get_db)):
    """Возвращает список спецификаций
    """
    sql_cmd = 'select BOM_LIST_ID as "id",\
                from BOM_LIST_S(0,?,0,0,?,0,0,0,0,?,\'\',0,0,0)'
    return dbcon.cursor().execute(
        sql_cmd, (contained_bom, descript, str_id)).fetchallmap()