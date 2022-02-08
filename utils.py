class Users:
    """
    Класс Запрос. Собирает информацию по текущему запросу для отправки затем в историю. При последующем запросе
    данные затираются ?????????????????????????????/ и сохраняется новый экземлпяр класс
    """
    users = dict()

    def __init__(self, datetime: str, user_id: str, city: str, city_id: str, count_hotel: int, perimeter: str,
                 photo: str, price: str, checkout: str, checkin: str, team: str, count_photo: int, req_photo: str,
                 answer: str):
        self.datetime = datetime  # время запроса
        self.user_id = user_id
        self.city = city  # город запроса
        self.city_id = city_id  # id города
        self.country: str = None  # страна запроса
        self.count_hotel = count_hotel  # количество отелей в запросе
        self.perimeter = perimeter  # удаленность от центра
        self.photo = photo  # наличие фото
        self.price = price  # цена в запросе
        self.checkout = checkout  # дата заезда
        self.checkin = checkin  # дата выезда
        self.answer = answer  # ответ по запросу
        self.team = team  # команда в запросе
        self.count_photo = count_photo  # количество фото в запросе
        self.req_photo = req_photo  # ссылки на фото
        Users.add_user(user_id, self)

    def __str__(self):
        return self.user_id

    @staticmethod
    def get_user(datetime: str, user_id: str, city: str, city_id: str, count_hotel: int, perimeter: str,
                 photo: str, price: str, checkout: str, checkin: str, team: str, count_photo: int, req_photo: str,
                 answer: str):
        if Users.users.get(user_id) is None:
            new_user = Users(datetime, user_id, city, city_id, count_hotel, perimeter, photo, price,
                             checkout, checkin, team, count_photo, req_photo, answer)
            return new_user
        return Users.users.get(user_id)

    @classmethod
    def add_user(cls, user_id, user):
        cls.users[user_id] = user
