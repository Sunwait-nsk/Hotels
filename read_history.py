from peewee import InternalError
from loader import logging
from models import Answer, History, dbhandle


@logging
def read() -> list:
    """
    Функция работы с базой данных history (история запросов) .
    Добавление строки БД с информацией по запросу и ответу по нему
    """
    with dbhandle:
        try:
            length_history = len(History.select())
            out = History.select()
            row_out = []
            for element in out:
                hotel = read_hotel(element.id_answer)
                if length_history > 5:
                    if element.id_answer >= length_history - 5:

                        row_out.append([element.commands, "{}".format(element.date), element.city,
                                        element.count_photo, hotel])
                else:
                    row_out.append([element.commands, "{}".format(element.date), element.city, element.count_photo,
                                    hotel])

            return row_out
        except InternalError as px:
            print(str(px))
            return []


@logging
def read_hotel(id_in: int) -> str:
    with dbhandle:
        try:
            out = Answer.select()
            row_answer = ''
            for element in out:
                if element.id_answer == id_in:
                    if not(element.name in row_answer):
                        row_answer += "{} {} {}\n".format(element.name, element.current, element.address)

            return row_answer
        except InternalError as px:
            print(str(px))
            return ''
