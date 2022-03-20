import current
from requests.exceptions import Timeout, ConnectionError
import requests
import json
from loader import logging
import loader
import re


@logging
def hotel_id(cls) -> str:
    """
    Функция по работе с API.
    На входе получает город и страну
    Выходные данные: ID города на сайте Hotel.com
    """
    # установочные данные
    plenty_destination_id = ''
    url = "https://hotels4.p.rapidapi.com/locations/v2/search"
    querystring = {"query": cls.city, "locale": "en_US", "currency": "USD"}
    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': loader.api_key
    }

    plenty_city = []
    # выполнение запроса по названию города cls.city
    # api_key - ключ к API документации
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=5)
        if response.status_code == 200:
            data = json.loads(response.text)
            for element in data['suggestions'][0]['entities']:
                if element['name'] == cls.city:
                    plenty_destination_id = element['destinationId']
                    plenty_city.append(element['name'])
    except Timeout:
        print('Ошибка таймаута')
    except ConnectionError:
        print('Ошибка соединения')
    return plenty_destination_id


@logging
def hotels_list(cls) -> tuple:
    """
        Функция по работе с API.
        На входе получает класс с запросом и признаком команды поиска
        Выходные данные: перечень отелей в виде списка. Если есть отметка о необходимости фотографий,
        то происходит вызов функции hotels_photo с поиском фотографий к каждому отелю
        Список с отелями содержит: название отеля, адрес, стоимость в руб, удаленность от центра, id отеля
        """
    # установочные данные
    answer = []
    url = "https://hotels4.p.rapidapi.com/properties/list"
    price_order = 'PRICE'
    if cls.team == '/highprice':
        price_order = 'PRICE_HIGHEST_FIRST'
    querystring = {
        "destinationId": cls.city_id,
        "pageNumber": "1",
        "pageSize": cls.count_hotel,
        "checkIn": cls.checkin,
        "checkOut": cls.checkout,
        "adults1": "1",
        "sortOrder": price_order,
        "locale": "en_US",
        "currency": "USD"}
    headers = {
            'x-rapidapi-host': "hotels4.p.rapidapi.com",
            'x-rapidapi-key': loader.api_key
        }
    # обработка запроса
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=20)
        if response.status_code != 200:
            print('Ошибка:')
            return 0, False
        else:
            data = json.loads(response.text)
            result_hotel = []
            number_answer = 0
            # обработка результата запроса и формирование списка отелей
            if data["data"]['body']['searchResults']['results']:
                for element in data["data"]['body']['searchResults']['results']:
                    number_answer += 1
                    remoteness = element['landmarks'][0]['distance']  # удаленность
                    current_hotel = current.diff_current(element['ratePlan']['price']['fullyBundledPricePerStay'])  # цена
                    url_hotels = url_hotel(cls, element['id'])  # формируем ссылку
                    try:
                        if element['address']["streetAddress"]:
                            result_hotel.append([element['name'], element['address']["streetAddress"], current_hotel,
                                                 remoteness, element['id'], url_hotels])
                            answer.append(hotels_photo(cls, element['name'], element['address']["streetAddress"],
                                                       current_hotel, remoteness, element['id'], url_hotels))
                    except KeyError:
                        result_hotel.append([element['name'], '', current_hotel, remoteness, element['id'], url_hotels])
                        print(str(element['name']), '', current_hotel, remoteness, element['id'], url_hotels)
                        answer.append(hotels_photo(cls, str(element['name']), '', current_hotel, remoteness, element['id'],
                                                   url_hotels))

                # ответ с фотографиями
                # возврат списка из отелей в виде [название, адрес, цена, id отеля, ссылка,[список фотографий]]
            if number_answer != cls.count_hotel:
                return number_answer, answer
            else:
                return cls.count_hotel, answer
    except Timeout:
        print('Ошибка таймаута')
    except ConnectionError:
        print('Ошибка соединения')


@logging
def hotels_list_bestdeal(cls) -> tuple:

    """
        Функция по работе с API для команды  bestdeal.
        На входе получает класс с запросом и признаком команды поиска
        Выходные данные: перечень отелей в виде списка. Если есть отметка о необходимости фотографий,
        то происходит вызов функции hotels_photo с поиском фотографий к каждому отелю
        Список с отелями содержит: название отеля, адрес, стоимость в руб, удаленность от центра, id отеля
        """
    # установочные данные
    answer = []
    url = "https://hotels4.p.rapidapi.com/properties/list"
    price_order = 'PRICE'
    if cls.team == '/highprice':
        price_order = 'PRICE_HIGHEST_FIRST'
    querystring = {
        "destinationId": cls.city_id,
        "pageNumber": "1",
        "pageSize": cls.count_hotel,
        "checkIn": cls.checkin,
        "checkOut": cls.checkout,
        "adults1": "1",
        "sortOrder": price_order,
        "locale": "en_US",
        "currency": "USD"}
    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': loader.api_key
    }
    # обработка запроса
    try:
        response = requests.get(url, headers=headers, params=querystring, timeout=20)
        if response.status_code != 200:
            print('Ошибка:')
            return 0, False
        else:
            data = json.loads(response.text)
            result_hotel = []
            number_answer = 0
            # обработка результата запроса и формирование списка отелей
            if data["data"]['body']['searchResults']['results']:
                for element in data["data"]['body']['searchResults']['results']:
                    number_answer += 1
                    remoteness = element['landmarks'][0]['distance']  # удаленность
                    current_hotel = current.diff_current(element['ratePlan']['price']['fullyBundledPricePerStay'])  # цена
                    url_hotels = url_hotel(cls, element['id'])  # формируем ссылку
                    try:
                        if int(cls.perimeter[0]) <= remoteness <= int(cls.perimeter[1]):
                            if int(cls.price[0]) <= current_hotel <= int(cls.price[1]):
                                if element['address']["streetAddress"]:
                                    result_hotel.append([element['name'], element['address']["streetAddress"],
                                                         current_hotel, remoteness, element['id'], url_hotels])
                                    answer.append(hotels_photo(cls, element['name'],
                                                               element['address']["streetAddress"], current_hotel,
                                                               remoteness, element['id'], url_hotels))
                    except KeyError:
                        result_hotel.append([element['name'], '', current_hotel, remoteness, element['id'], url_hotels])
                        answer.append(hotels_photo(cls, element['name'], '', current_hotel, remoteness, element['id'],
                                                   url_hotels))

                # ответ с фотографиями
                # возврат списка из отелей в виде [название, адрес, цена, id отеля, ссылка,[список фотографий]]
            if number_answer != cls.count_hotel:
                return number_answer, answer
            else:
                return cls.count_hotel, answer
    except Timeout:
        print('Ошибка таймаута')
    except ConnectionError:
        print('Ошибка соединения')



@logging
def hotels_photo(cls, name: str, address: str, current: str, remoteness: str, id_hotel: str, url_h: str) -> list:
    """
    Функция по работе с API.
    На входе получает класс с запросом и признаком команды поиска
    Выходные данные: перечень отелей в виде списка. Если есть отметка о необходимости фотографий,
    то происходит вызов функции hotels_photo с поиском фотографий к каждому отелю
    Список с отелями содержит: название отеля, адрес, стоимость в руб, удаленность от центра, id отеля
    """
    # установочные данные
    url = "https://hotels4.p.rapidapi.com/properties/get-hotel-photos"
    # по всем отелям подгружаем фотографии по id - 4 элемент в списке
    querystring = {"id": id_hotel}
    headers = {
        'x-rapidapi-host': "hotels4.p.rapidapi.com",
        'x-rapidapi-key': loader.api_key
    }
    image_hotel = []
    count_photo = 0
    response = requests.get(url, headers=headers, params=querystring)
    data = json.loads(response.text)
    plenty = []  # список всех фотографий
    # обработка полученного результата запроса
    for element in data['hotelImages']:
        plenty.append(element["baseUrl"])
    if cls.photo == 'да' or cls.photo == 'yes':
        for i_count in range(int(cls.count_photo)):
            image_hotel.append(re.sub(r'{size}', 'y', plenty[i_count]))  # установка размера фото
            count_photo = cls.count_photo
    result_photo = [cls.answer, cls.count_hotel, name, current, remoteness, address, id_hotel, url_h,
                    count_photo, image_hotel]
    return result_photo


def url_hotel(cls, id_hotel) -> str:
    """
    Формирование текстовой ссылки на отель на сайте Hotels.com
    https://ru.hotels.com/ho203480/?q-check-in=2022-01-08&q-check-out=2022-01-15&q-rooms=1&q-room-0-adults=1&q-room-0-children=0
    """
    day, month, year = cls.checkout.day, cls.checkout.month, cls.checkout.year
    checkout = "-".join([str(year), str(month), str(day)])
    day, month, year = cls.checkin.day, cls.checkin.month, cls.checkin.year
    checkin = "-".join([str(year), str(month), str(day)])
    pattern_url = "https://hotels.com/ho{}/?q-check-in={}&q-check-out={}&" \
                  "q-rooms=1&q-room-0-adults=1&q-room-0-children=0".format(id_hotel, checkin, checkout)
    return pattern_url
