import telebot
from dotenv import load_dotenv
import os
import functools
from typing import Callable, Any


load_dotenv('.env')
bot = telebot.TeleBot(os.getenv('TOKEN'))
api_key = os.getenv('rapidapi_key')


def logging(called: Callable) -> Callable:
    """Декоратор. Логирование работы функций
    """
    @functools.wraps(called)
    def wrapped_function(*args, **kwargs) -> Any:
        result = ''

        print("Вызывается функция {}\tПозиционные аргументы{}\tИменованные аргументы".format(called, args, kwargs))
        try:

            result = called(*args, **kwargs)
            print('функция {} завершилась успешно'.format(called.__name__))

        except SyntaxError:

            print('Функция не найдена')
        return result
    return wrapped_function


def documentation_function(function_out: Callable) -> str:
    """функция проверяет наличие документации в функции
    аргументы: проверяемая функция
    Возвращает документацию функции либо ошибку SyntaxError при ее отсутствии"""
    if function_out.__doc__:
        return function_out.__doc__
    else:
        raise SyntaxError
