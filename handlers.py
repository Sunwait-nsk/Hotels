from loader import logging, bot
from utils import Users
from typing import Any
import current
import rapidapi
import geo_city
import add_history
import add_answer
import read_history


@logging
def lowprice(message: Any) -> None:
    """
    Функция для обработки команды lowprice.
    Запускает алгоритм функций для этой команды
    """
    user = Users(message.from_user.id)  # добавили пользователя по id
    user.team = '/lowprice'
    bot.send_message(message.from_user.id, "Введите город")
    bot.register_next_step_handler(message, get_city)


@logging
def highprice(message: Any) -> None:
    """
        Функция для обработки команды highprice.
        Запускает алгоритм функций для этой команды
        """
    user = Users(message.from_user.id)
    user.team = '/highprice'
    bot.send_message(message.from_user.id, "Введите город")
    bot.register_next_step_handler(message, get_city)


@logging
def bestdeal(message: Any) -> None:
    """
            Функция для обработки команды bestdeal.
            Запускает алгоритм функций для этой команды
            """
    user = Users(message.from_user.id)
    user.team = '/bestdeal'
    bot.send_message(message.from_user.id, "Введите город")
    bot.register_next_step_handler(message, get_city)


@logging
def history(message: Any) -> None:
    """
        Обработка команды /history
    """
    request_user = Users(message.from_user.id)
    request_user.team = '/history'
    request_user.answer = add_history.add_history(user_id=request_user.user_id,
                                                  team=request_user.team,
                                                  city=request_user.city,
                                                  count_hotel=request_user.count_hotel,
                                                  checkin=request_user.checkin,
                                                  checkout=request_user.checkout,
                                                  photo=request_user.photo,
                                                  count_photo=request_user.count_photo,
                                                  price=request_user.price,
                                                  perimeter=request_user.perimeter)  # добавляем в БД history запрос
    bot.send_message(message.from_user.id, 'Последние 5 записей поиска')
    # вывод ответов по последним 5 запросам
    number = 0
    row_info = read_history.read()
    for element in row_info:
        row = 'Дата  - {} ---- команда - {}\nГород - {} \nОтели - {}\n'.\
            format(element[1], element[0], element[2], element[4])
        count_photo = int(element[3])
        if count_photo != 0:
            number += 1
            if number % count_photo == 0:
                bot.send_message(message.from_user.id, row)
        else:
            bot.send_message(message.from_user.id, row)


@logging
def get_city(message: Any) -> None:
    """
    Обработка названия города и передача дальнейшего управления следующему модулю
    """
    user = Users.get_user(message.from_user.id)
    user.city, user.country = '', ''
    # Обращаемся к БД городов, что бы получить список город на русском и страна на английском
    # заодно проверяем корректность названия города. В противном случае бот запрашивает город заново
    user.country = geo_city.city(message.text)
    user.city = message.text
    if user.country != '':
        if user.team == '/bestdeal':
            bot.send_message(message.from_user.id,
                             'Введите диапозон цен, например 1000 - 2000')
            bot.register_next_step_handler(message, get_current_hotel)
        else:
            bot.send_message(message.from_user.id,
                             'Количество отелей, которые необходимо вывести в результате (не более 25)')
            bot.register_next_step_handler(message, get_count_hotel)
    else:
        bot.send_message(message.from_user.id, "Город введен некорректно или не найден. Введите город?")
        bot.register_next_step_handler(message, get_city)


@logging
def get_current_hotel(message: Any) -> None:
    """фунция запрос диапозона цен отелей """
    user = Users.get_user(message.from_user.id)
    user.price = current.part_row(message.text)
    bot.send_message(message.from_user.id,
                     'Введите удаленность, например 1 - 2')
    bot.register_next_step_handler(message, get_length)


@logging
def get_length(message: Any) -> None:
    """фунция запрос диапозона расстояний до центра """
    request_user = Users.get_user(message.from_user.id)
    request_user.perimeter = current.part_row(message.text)
    bot.send_message(message.from_user.id,
                     'Количество отелей, которые необходимо вывести в результате (не более 25)')
    bot.register_next_step_handler(message, get_count_hotel)


@logging
def get_count_hotel(message: Any) -> None:
    """фунция запрос количества отелей """
    request_user = Users.get_user(message.from_user.id)
    request_user.count_hotel = ''
    request_user.count_hotel = message.text
    # если количество отелей больше 25 или введен некорректно, то бот запрашивает информацию еще раз
    if request_user.count_hotel.isdigit() and int(request_user.count_hotel) <= 25:
        bot.send_message(message.from_user.id, 'Дата заезда по формату дата-месяц-год')
        bot.register_next_step_handler(message, get_date_in)
    else:
        bot.send_message(message.from_user.id, 'Количество отелей введено некорректно, введите цифрами пожалуйста. '
                                               'Не более 25')
        bot.register_next_step_handler(message, get_count_hotel)


@logging
def get_date_in(message: Any) -> None:
    """функция запроса даты заезда в формате день-месяц-год. Форма разделителя не важна"""
    request_user = Users.get_user(message.from_user.id)
    request_user.checkin = ''
    # Проверка даты на корректность. Формат день-месяц-год. В случае некорректности вернуть пустую строку в класс
    request_user.checkin = current.date_in_out(message.text)
    if request_user.checkin != '' and request_user.checkin:
        bot.send_message(message.from_user.id, 'Дата выезда в формате день-месяц-год')
        bot.register_next_step_handler(message, get_date_out)
    else:
        bot.send_message(message.from_user.id, 'Некоректный ввод. Вводим дату по формату дата-месяц-год')
        bot.register_next_step_handler(message, get_date_in)


@logging
def get_date_out(message: Any) -> None:
    """
    функция обработки запроса даты выезда в формате день-месяц-год. Форма разделителя не важна
    на вход поступает сообщение бота с датой
    """
    request_user = Users.get_user(message.from_user.id)
    request_user.checkout = ''
    # Проверка даты на корректность. Формат день-месяц-год. В случае некорректности вернуть пустую строку в класс
    request_user.checkout = current.date_in_out(message.text)
    if request_user.checkout != '' and request_user.checkout:
        bot.send_message(message.from_user.id,
                         'Необходимость загрузки и вывода фотографий для каждого отеля (“Да/Нет”)')
        bot.register_next_step_handler(message, get_answer_photo)
    else:
        bot.send_message(message.from_user.id, 'Некоректный ввод. Вводим дату по формату дата-месяц-год')
        bot.register_next_step_handler(message, get_date_out)


@logging
def get_answer_photo(message: Any) -> None:
    """
    функция обработки запроса о необходимости подгрузки фотографий отеля
    на вход поступает сообщение бота с ответом "Да/нет" (не важно какими буквами)
    """
    request_user = Users.get_user(message.from_user.id)
    request_user.photo = ''
    request_user.photo = message.text.lower()
    if request_user.photo == 'да' or request_user.photo == 'yes':
        bot.send_message(message.from_user.id, 'Количество фотографий')
        bot.register_next_step_handler(message, get_photo)
    elif request_user.photo == 'нет' or request_user.photo == 'no':
        get_answer(request_user)
    else:
        bot.send_message(message.from_user.id, 'Некорректный ответ. Пожалуйста введит -“Да/Нет”')
        bot.register_next_step_handler(message, get_answer_photo)


@logging
def get_photo(message: Any) -> None:
    """функция обработки количества фотографий отеля"""
    request_user = Users.get_user(message.from_user.id)
    if message.text.isdigit():
        request_user.count_photo = int(message.text)
        get_answer(request_user)


@logging
def get_answer(cls) -> None:
    answer = False
    key_user = add_history.add_history(user_id=cls.user_id, team=cls.team, city=cls.city, count_hotel=cls.count_hotel,
                                       checkin=cls.checkin, checkout=cls.checkout, photo=cls.photo,
                                       count_photo=cls.count_photo, price=cls.price, perimeter=cls.perimeter)

    if key_user:
        if not answer:
            cls.city_id = rapidapi.hotel_id(cls)
            cls.count_hotel, answer = rapidapi.hotels_list(cls)
            for i_count in range(int(cls.count_hotel)):
                if cls.photo == 'да':
                    row = '{}\nстоимость - {}\nудаленность от центра города - {}\nадрес - {}\nссылка на сайте - {}\n'.\
                        format(answer[i_count][2], answer[i_count][3], answer[i_count][4],
                               answer[i_count][5], answer[i_count][7])
                    bot.send_message(cls.user_id, row)
                    for i_photo in range(int(cls.count_photo)):
                        bot.send_photo(cls.user_id, answer[i_count][9][i_photo])
                        add_answer.add_answer(key_user, answer[i_count][6], int(cls.count_hotel), answer[i_count][2],
                                              answer[i_count][3], answer[i_count][4], answer[i_count][5],
                                              answer[i_count][7], cls.count_photo, answer[i_count][9][i_photo])
                else:
                    row = '{}\nстоимость - {}\nудаленность от центра города - {}\nадрес - {}\nссылка на сайте - {}\n'.\
                        format(answer[i_count][2], answer[i_count][3], answer[i_count][4],
                               answer[i_count][5], answer[i_count][7])
                    bot.send_message(cls.user_id, row)
                    add_answer.add_answer(key_user, answer[i_count][6], int(cls.count_hotel), answer[i_count][2],
                                          answer[i_count][3], answer[i_count][4], answer[i_count][5],
                                          answer[i_count][7], cls.count_photo, '')
        else:

            photo_hotel = []
            if answer:
                flag = len(answer)
            else:
                flag = []
            for i_count in range(flag):
                if cls.photo == 'да':
                    if (i_count + 1) % cls.count_photo == 0:
                        row = '{}\nстоимость - {}\nудаленность от центра города - {}\nадрес - {}\n' \
                              'ссылка на сайте - {}\n'.\
                            format(answer[i_count]['name'], answer[i_count]['current'], answer[i_count]['remoteness'],
                                   answer[i_count]['address'], answer[i_count]['req_web'])
                        bot.send_message(cls.user_id, row)
                        photo_hotel.append(answer[i_count]['req_photo'])
                        photo_hotel = []
                        for photo in photo_hotel:
                            bot.send_photo(cls.user_id, photo)
                    else:
                        photo_hotel.append(answer[i_count]['req_photo'])
                else:
                    row = '{}\nстоимость - {}\nудаленность от центра города - {}\nадрес - {}\nссылка на сайте - {}\n'. \
                        format(answer[i_count]['name'],
                               answer[i_count]['current'],
                               answer[i_count]['remoteness'],
                               answer[i_count]['address'],
                               answer[i_count]['req_web'])
                    bot.send_message(cls.user_id, row)
