import telebot
from dotenv import load_dotenv
import os
import functools
from typing import Callable, Any


load_dotenv('.env')
bot = telebot.TeleBot(os.getenv('TOKEN'))
api_key = os.getenv('rapidapi_key')
password = os.getenv('password')
geo_key = os.getenv('geo_key')

def logging(called: Callable) -> Callable:
    """Декоратор. Логирование работы функций
    """
    @functools.wraps(called)
    def wrapped_function(*args, **kwargs) -> Any:
        result = ''
        with open("sample.log", 'a', encoding="utf-8") as log_file:
            log_file.write("Вызывается функция {}\tПозиционные аргументы{}\tИменованные аргументы\n".
                           format(called, args, kwargs))
            try:
                result = called(*args, **kwargs)
                log_file.write('функция {} завершилась успешно\n'.format(called.__name__))
            except SyntaxError:
                log_file.write('Функция не найдена\n')
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
