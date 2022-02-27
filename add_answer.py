from loader import logging
from models import Answer, dbhandle


@logging
def add_answer(id_answer: int, id_hotel: str, count_hotel: int, name: str, current: str, remoteness: str,
               address: str, req_web: str, count_photo: int, req_photo: str) -> bool:
    """
    Функция работы с базой данных answer (история ответов) .
    добавление в бд ответа по запросу
    """
    with dbhandle:
        try:
            if current != '':
                current = str(current[0]) + ' - ' + str(current[1])
            if remoteness != '':
                remoteness = str(remoteness[0]) + ' - ' + str(remoteness[1])
            row = Answer(id_answer=id_answer, id_hotel=id_hotel, count_hotel=count_hotel, name=name,
                         current=current, remoteness=remoteness, address=address, req_web=req_web,
                         count_photo=count_photo, req_photo=req_photo)
            row.save()
            return id_answer
        except InternalError as px:
            print(str(px))
            return False

