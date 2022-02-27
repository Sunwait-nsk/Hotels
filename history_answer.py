from peewee import InternalError
from loader import logging
from models import History, dbhandle


@logging
def find_answer() -> bool:
    """
    Функция работы с базой данных history (история запросов) .
    Добавление строки БД с информацией по запросу и ответу по нему
    """
    with dbhandle:
        try:
            out = History.select()
            print(len(out))
            id_answer = History.get(History.user_id == len(out))
            return id_answer
        except InternalError as px:
            print(str(px))
            return False
