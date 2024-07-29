from typing import Dict, List
from fastapi import status
from fastapi import APIRouter, Depends, HTTPException, Path

import fdb
from pydantic import BaseModel

from ..dependencies import get_db

router = APIRouter()


def execute_sql_query(dbcon, sql_cmd, *args):
    cursor = dbcon.cursor()
    cursor.execute(sql_cmd, args)
    field_names = [desc[0] for desc in cursor.description]
    return cursor, field_names


def get_all_dict_results(dbcon, sql_cmd, *args):
    cursor, field_names = execute_sql_query(dbcon, sql_cmd, *args)
    return [dict(zip(field_names, row)) for row in cursor]


def raise_404_if_none(data):
    if not data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Записей не найдено")
    

@router.get('/api/device_card/serial_number/{serial_number}/nomenclature',
            summary='Получение номенклатуры по серийному номеру',
            tags=['device_card'])
def get_nomenclature(serial_number: str = Path(title='Серийный номер'),
                     dbcon: fdb.Connection = Depends(get_db)):
    sql_cmd = """select 123
                where stp.sn_text = ?"""
    nomenclature = dbcon.cursor().execute(sql_cmd, (serial_number,)).fetchonemap()

    raise_404_if_none(nomenclature)

    return nomenclature


@router.get('/api/device_card/serial_number/{serial_number}/repairs_with_bitrix_deal',
            summary='Получение отпусков в производство по серийному номеру',
            tags=['device_card'])
def get_repair(serial_number: str = Path(title='Серийный номер'),
               dbcon: fdb.Connection = Depends(get_db)):
    repairs = get_repairs_by_serial_number(serial_number, dbcon)

    repairs = merge_bitrix_deals_by_sn(repairs, serial_number, dbcon)

    return repairs


def get_repairs_by_serial_number(serial_number: str, dbcon: fdb.Connection) -> List[Dict]:
    sql_cmd = """select 123(?) repairs"""
    results = get_all_dict_results(dbcon, sql_cmd, serial_number)
    return results


def merge_bitrix_deals_by_sn(repairs: List[Dict], serial_number: str, dbcon: fdb.Connection) -> List[Dict]:
    sql_cmd = """select 1"""
    bitrix_deals = get_all_dict_results(dbcon, sql_cmd, serial_number)

    return update_bitrix_deals(repairs, bitrix_deals)


def update_bitrix_deals(repairs: List[Dict], bitrix_deals: List[Dict]) -> List[Dict]:
    for item in repairs:
        item.setdefault('bitrixDeals', [])

    for repair in repairs:
        for bitrix_deal in bitrix_deals:
            if repair['repairOrderId'] == bitrix_deal['repairOrderId']:
                repair['bitrixDeals'].append({'number': bitrix_deal['number']})

    return repairs


@router.get('/api/device_card/serial_number/{serial_number}/order',
            summary='Получение заказа по серийному номеру',
            tags=['device_card'])
def get_order(serial_number: str = Path(title='Серийный номер'),
              dbcon: fdb.Connection = Depends(get_db)):
    sql_cmd = """select c"""
    order = dbcon.cursor().execute(sql_cmd, (serial_number,)).fetchonemap()

    raise_404_if_none(order)

    return order


@router.get('/api/device_card/firms/{firm}/repairs_order',
            summary='Получение возвратов на ремонт по фирме',
            tags=['device_card'])
def get_repair_order(firm: int = Path(title='Id фирмы'),
                     dbcon: fdb.Connection = Depends(get_db)):
    sql_cmd = """SELECT 
                    WHERE 123 = 12"""
    return dbcon.cursor().execute(sql_cmd, (firm,)).fetchallmap()


@router.get('/api/device_card/repair/{repair_id}/repairs_order',
            summary='Получение возврата на ремонт по отпуску в производство',
            tags=['device_card'])
def get_repair_order(repair_id: int = Path(title='Id документа отпуска в производство'),
                     dbcon: fdb.Connection = Depends(get_db)):
    sql_cmd = """select dh.doc_id as "id",                       
                where 12 = 12"""
    repair_order = dbcon.cursor().execute(sql_cmd, (repair_id,)).fetchonemap()

    raise_404_if_none(repair_order)

    return repair_order


@router.get('/api/device_card/repair/{repair_id}',
            summary='Получение информации о ремонте',
            tags=['device_card'])
def get_repair_info(repair_id: int = Path(title='Id документа отпуск на ремонт'),
                    dbcon: fdb.Connection = Depends(get_db)):
    sql_cmd = """SELECT SERIAL_NUMBER AS "serialNumber",
                        from 123(?)"""
    repair = dbcon.cursor().execute(sql_cmd, (repair_id,)).fetchonemap()

    raise_404_if_none(repair)

    return repair


@router.get('/api/device_card/repairs_order/{repair_order_id}/repairs',
            summary='Получение отпусков в ремонт по возврату на ремонт',
            tags=['device_card'])
def get_repair_by_repair_order(repair_order_id: int = Path(title='Id документа возврат на ремонт'),
                               dbcon: fdb.Connection = Depends(get_db)):
    sql_cmd = """SELECT SERIAL_NUMBER AS "serialNumber",
                        from 123(?)"""

    return dbcon.cursor().execute(sql_cmd, (repair_order_id,)).fetchallmap()


@router.get('/api/device_card/repairs_order/{repair_order_id}/repairs_with_bitrix_deal',
            summary='Получение отпусков в ремонт по возврату на ремонт',
            tags=['device_card'])
def get_repair_by_repair_order(repair_order_id: int = Path(title='Id документа возврат на ремонт'),
                               dbcon: fdb.Connection = Depends(get_db)):
    sql_cmd = """SELECT SERIAL_NUMBER AS "serialNumber",
                        from 123(?)"""
    repairs = get_all_dict_results(dbcon, sql_cmd, repair_order_id)

    repairs = merge_bitrix_deals_by_repair_order(
        repairs, repair_order_id, dbcon)

    return repairs


def merge_bitrix_deals_by_repair_order(repairs: List[Dict], repair_order_id: int, dbcon: fdb.Connection) -> List[Dict]:
    sql_cmd = """select bitrix_deal.REPAIR_ORDER_ID as "repairOrderId", 
                    bitrix_deal.DEAL_NUMBER as "number" 
                from 123(?) bitrix_deal"""
    bitrix_deals = get_all_dict_results(dbcon, sql_cmd, repair_order_id)

    return update_bitrix_deals(repairs, bitrix_deals)


@router.get('/api/device_card/repairs_order/{repair_order_id}/bitrix_deal',
            summary='Получение номеров сделок в битриксе',
            tags=['device_card'])
def get_bitrix_deal(repair_order_id: int = Path(title='Id документа возврат на ремонт'),
                    dbcon: fdb.Connection = Depends(get_db)):
    sql_cmd = """SELECT rl.deal_number as "number"
                    from 123 rl
                    where rl.repair_id = ?"""
    return dbcon.cursor().execute(sql_cmd, (repair_order_id,)).fetchallmap()


class BitrixDeal(BaseModel):
    number: int


@router.post('/api/device_card/repairs_order/{repair_order_id}/bitrix_deal',
             summary='Добавление привязки номера сделки к заказу в ремонт',
             tags=['device_card'])
def post_bitrix_deal(bitrix_deal: BitrixDeal,
                     repair_order_id: int = Path(
                         title='Id документа возврат на ремонт'),
                     dbcon: fdb.Connection = Depends(get_db)):
    sql_cmd = """SELECT rl.res_id
                    from 123(?,?) rl"""

    ans = dbcon.cursor().execute(sql_cmd, (repair_order_id, bitrix_deal.number)).fetchone()
    if ans is None or int(ans[0]) == 0:
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Сделка битрикс не была создана.")
    return ans[0]


@router.delete('/api/device_card/repairs_order/{repair_order_id}/bitrix_deal/{deal_number}',
               summary='Удаление номера сделки привязоного к заказу в ремонт',
               tags=['device_card'])
def delete_bitrix_deal(repair_order_id: int = Path(title='Id документа возврат на ремонт'),
                       deal_number: int = Path(title='Номер сделки в битрикс'),
                       dbcon: fdb.Connection = Depends(get_db)):
    cur = dbcon.cursor()
    cur.callproc('REPAIR_BITRIX_DEAL_LINK_D', [repair_order_id, deal_number])

    delete_result = cur.fetchone()
    if delete_result is None or int(delete_result[0]) == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Не удалено. Не существует связки сделки битрикс и заказа в ремонт.")


@router.get('/api/device_card/bitrix_deal/{deal_number}/repairs_order',
            summary='Получение возвратов на ремонт по номеру сделки в битрикс',
            tags=['device_card'])
def get_repair_order(deal_number: int = Path(title='Номер сделки'),
                     dbcon: fdb.Connection = Depends(get_db)):
    sql_cmd = """SELECT dh.doc_id AS "id",
                WHERE 1=1"""
    return dbcon.cursor().execute(sql_cmd, (deal_number,)).fetchallmap()
