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
def read() -> list:
    """
    Функция работы с базой данных history (история запросов) .
    Добавление строки БД с информацией по запросу и ответу по нему
    """
    try:
        dbhandle.connect()
        length_history = len(History.select())
        if length_history > 5:
            length_out = length_history - 5
        else:
            length_out = length_history
        print(length_out)
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
    finally:
        dbhandle.close()


@ logging
def read_hotel(id: int) -> list:
    try:
        out = Answer.select()
        row_answer = ''
        for element in out:
            if element.id_answer == id:
                row_answer += "{} {} {}\n".format(element.name, element.current, element.address)
        return row_answer
    except InternalError as px:
        print(str(px))
        return []
    finally:
        dbhandle.close()


