from peewee import *
import datetime
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


class History(BaseModel):
    id = PrimaryKeyField(null=False)
    user_id = CharField(max_length=25)
    commands = CharField(max_length=15)
    date = DateTimeField(default=datetime.datetime.now())
    id_answer = IntegerField()
    city = CharField(max_length=150)
    count_hotel = IntegerField()
    datein = CharField(max_length=15)
    dateout = CharField(max_length=15)
    photo = CharField(max_length=3)
    count_photo = IntegerField()
    price = CharField(max_length=45)
    perimeter = CharField(max_length=45)

    class Meta:
        db_table = "history"
        order_by = ('id',)


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
def find_answer() -> bool:
    """
    Функция работы с базой данных history (история запросов) .
    Добавление строки БД с информацией по запросу и ответу по нему
    """
    try:
        dbhandle.connect()
        out = History.select()
        print(len(out))
        id = History.get(History.user_id == len(out))
        print(id)

    except InternalError as px:
        print(str(px))
        return False
    finally:
        dbhandle.close()


find_answer()