from peewee import InternalError
from loader import logging
from models import History, dbhandle


@logging
def add_history(user_id, team, city, count_hotel, checkin, checkout, photo, count_photo, price,
                perimeter) -> bool:
    """
    Функция работы с базой данных history (история запросов) .
    Добавление строки БД с информацией по запросу и id ответа по нему
    """
    with dbhandle:
        try:
            answer = len(History.select()) + 1
            if team == '/bestdeal' and price != '':
                price = str(price[0]) + ' - ' + str(price[1])
                if perimeter != '':
                    perimeter = str(perimeter[0]) + ' - ' + str(perimeter[1])
            row = History(user_id=user_id, commands=team, id_answer=answer, city=city, count_hotel=count_hotel,
                          datein=checkin, dateout=checkout, photo=photo, count_photo=count_photo, price=price,
                          perimeter=perimeter)
            row.save()
            return answer
        except InternalError as px:
            print(str(px))
            return False
