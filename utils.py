import datetime


class Users:
    """
    Класс Запрос. Собирает информацию по текущему запросу для отправки затем в историю. При последующем запросе
    данные затираются ?????????????????????????????/ и сохраняется новый экземлпяр класс
    """
    users = dict()

    def __init__(self, user_id: str):
        self.datetime = datetime.datetime.now()  # время запроса
        self.user_id = user_id
        self.city: str = None  # город запроса
        self.city_id: str = None  # id города
        self.country: str = None  # страна запроса
        self.count_hotel = 0  # количество отелей в запросе
        self.perimeter = ''  # удаленность от центра
        self.photo = None  # наличие фото
        self.price = ''  # цена в запросе
        self.checkout = None  # дата заезда
        self.checkin = None  # дата выезда
        self.answer = None  # ответ по запросу
        self.team = None  # команда в запросе
        self.count_photo = 0  # количество фото в запросе
        self.req_photo = None  # ссылки на фото
        Users.add_user(user_id, self)

    def __str__(self):
        return self.user_id

    @staticmethod
    def get_user(user_id: str):
        if Users.users.get(user_id) is None:
            new_user = Users(user_id)
            return new_user
        return Users.users.get(user_id)

    @classmethod
    def add_user(cls, user_id, user):
        cls.users[user_id] = user
