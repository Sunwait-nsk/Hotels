import peewee
from loader import logging
from models import History, Answer, dbhandle


@logging
def find_answer(team, city, count, checkin, checkout, photo, count_photo, price,
                perimeter) -> bool:
    """
    Функция работы с базой данных history (история запросов) .
    Добавление строки БД с информацией по запросу и ответу по нему
    """
    with dbhandle:
        try:
            out = History.select()
            row_1 = [team, city, count, checkin, checkout, photo, count_photo, price, perimeter]
            answer = -1
            for element in out:
                if row_1 == [element.commands, element.city, element.count_hotel, element.datein, element.dateout,
                             element.photo, element.count_photo, element.price, element.perimeter]:
                    answer = element.id_answer
            if answer != -1:
                row = models.Answer.get(Answer.id_answer == answer)
                rows = [row.id_answer, row.count_hotel, row.name, row.current, row.remoteness, row.address, row.req_web,
                        row.count_photo, row.req_photo]
                return rows
            else:
                return False
        except InternalError as px:
            print(str(px))
            return False
