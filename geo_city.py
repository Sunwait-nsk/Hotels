from peewee import *
from loader import logging
from dotenv import load_dotenv
import os


"""
Работа с БД. возвращает страну города на английском языке
Создана для корректности и более точного поиска в дальнейшем на сайте с API
На вход поступает город name_city на русском языке, возвращает город на русском и страну country_en на англ.
Используется БД с основными городами всех стран
Дополнительно может вернуть город на английском. Поле в БД - CITY_EN
"""
load_dotenv('.env')
password = os.getenv('password')
user = 'root'
db_name = 'city_db'
dbhandle = MySQLDatabase(db_name,
                         user=user,
                         password=password,
                         host='localhost')


class BaseModel(Model):
    class Meta:
        database = dbhandle


class City(BaseModel):
    id = PrimaryKeyField(null=False)
    country_en = CharField(max_length=255)
    region_en = CharField(max_length=255)
    city_en = CharField(max_length=255)
    country = CharField(max_length=255)
    region = CharField(max_length=255)
    city = CharField(max_length=255)
    lat = CharField(max_length=255)
    lng = CharField(max_length=255)
    population = IntegerField()

    class Meta:
        db_table = "geo"
        order_by = ('city',)


def find_element_answer(name: str) -> str:
    name = name.capitalize()
    city = City.get(City.city == name)
    return city.country


@logging
def city(name: str) -> str:
    try:
        dbhandle.connect()
        return find_element_answer(name)
    except InternalError as px:
        print(str(px))
        return ''
    finally:
        dbhandle.close()

