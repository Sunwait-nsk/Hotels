from peewee import InternalError
from loader import logging
from models import City, dbhandle_city


"""
Работа с БД. возвращает страну города на английском языке
Создана для корректности и более точного поиска в дальнейшем на сайте с API
На вход поступает город name_city на русском языке, возвращает город на русском и страну country_en на англ.
Используется БД с основными городами всех стран
Дополнительно может вернуть город на английском. Поле в БД - CITY_EN
"""


@logging
def city(name: str) -> str:
    with dbhandle_city:
        try:
            name = name.capitalize()
            city_name = City.get(City.city == name)
            return city_name.country
        except InternalError as px:
            print(str(px))
            return ''
