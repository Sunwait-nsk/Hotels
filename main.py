from loader import bot, api_key
import handlers
import bd



@bot.message_handler(content_types=['text'])
def start(message) -> None:
    """
    Основной алгоритм бота. Алгоритм работает только при 6 командах,
    в остальных случаях просит ввести команду снова
    Параметры: словарь бота - message
    Подгружается модуль handlers для обработки соответствующей команды бота
    """
    if message.text == '/help' or message.text == '/start':
        bot.send_message(message.from_user.id, "/lowprice — вывод самых дешёвых отелей в городе, \n"
                                               "/highprice — вывод самых дорогих отелей в городе,\n"
                                               "/bestdeal — вывод отелей, наиболее подходящих по цене и "
                                               "расположению от центра. \n"
                                               "/history — вывод истории поиска отелей\n"
                                               "любой символ  - для вывода меню")
    elif message.text == '/lowprice':
        handlers.lowprice(message)
    elif message.text == '/highprice':
        handlers.highprice(message)
    elif message.text == '/bestdeal':
        handlers.bestdeal(message)
    elif message.text == '/history':
        handlers.history(message)
    else:
        bot.send_message(message.from_user.id, "/lowprice — вывод самых дешёвых отелей в городе, \n"
                                               "/highprice — вывод самых дорогих отелей в городе,\n"
                                               "/bestdeal — вывод отелей, наиболее подходящих по цене и "
                                               "расположению от центра. \n"
                                               "/history — вывод истории поиска отелей")


bot.polling()
