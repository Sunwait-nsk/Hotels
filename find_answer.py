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
def find_answer(team, city, count, checkin, checkout, photo, count_photo, price,
                perimeter) -> bool:
    """
    Функция работы с базой данных history (история запросов) .
    Добавление строки БД с информацией по запросу и ответу по нему
    """
    try:
        dbhandle.connect()
        out = History.select()
        row_1 = [team, city, count, checkin, checkout, photo, count_photo, price, perimeter]
        answer = -1
        for element in out:
            if row_1 == [element.commands, element.city, element.count_hotel, element.datein, element.dateout,
                         element.photo, element.count_photo, element.price, element.perimeter]:
                print(element.user_id, element.commands, element.city, element.count_hotel)
                print(element.id_answer)

                answer = element.id_answer
        if answer != -1:
            row = Answer.get(Answer.id_answer == answer)
            rows = [row.id_answer, row.count_hotel, row.name, row.current, row.remoteness, row.address, row.req_web,
                    row.count_photo, row.req_photo]
            return rows
        else:
            return False
    except InternalError as px:
        print(str(px))
        return False
    finally:
        dbhandle.close()
