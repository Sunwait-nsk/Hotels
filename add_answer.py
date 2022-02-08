from peewee import *
from loader import logging
from dotenv import load_dotenv
import os


load_dotenv('.env')
password = os.getenv('password')
user = 'root'
db_name = 'history'
dbhandle = MySQLDatabase(db_name,
                         user=user,
                         password=password,
                         host='localhost')


class BaseModel(Model):
    class Meta:
        database = dbhandle


class Answer(BaseModel):
    id = PrimaryKeyField(null=False)
    id_answer = IntegerField(null=False)
    id_hotel = CharField(max_length=25)
    count_hotel = IntegerField(null=False)
    name = CharField(max_length=100)
    current = CharField(max_length=45)
    remoteness = CharField(max_length=45)
    address = CharField(max_length=150)
    req_web = CharField(max_length=250)
    count_photo = IntegerField()
    req_photo = CharField(max_length=300)

    class Meta:
        db_table = "answer"
        order_by = ('id_answer',)


@logging
def add_answer(id_answer: int, id_hotel: str, count_hotel: int, name: str, current: str, remoteness: str,
               address: str, req_web: str, count_photo: int, req_photo: str) -> bool:
    """
    Функция работы с базой данных history (история запросов) .
    Добавление строки БД с информацией по запросу и ответу по нему
    """
    try:
        dbhandle.connect()
        Answer.create_table()
        if current != '':
            current = str(current[0]) + ' - ' + str(current[1])
        if remoteness != '':
            remoteness = str(remoteness[0]) + ' - ' + str(remoteness[1])
        row = Answer(id_answer=id_answer, id_hotel=id_hotel, count_hotel=count_hotel, name=name, current=current,
                     remoteness=remoteness, address=address, req_web=req_web, count_photo=count_photo,
                     req_photo=req_photo)
        row.save()
        print(id_answer)
        return id_answer
    except InternalError as px:
        print(str(px))
        return False
    finally:
        dbhandle.close()
