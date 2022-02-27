import datetime
import loader
from peewee import MySQLDatabase, Model, PrimaryKeyField, IntegerField, CharField, DateTimeField


password = loader.password
user = 'root'
db_name = 'history'
dbhandle = MySQLDatabase(db_name,
                         user=user,
                         password=password,
                         host='localhost')

dbhandle_city = MySQLDatabase('city_db',
                              user=user,
                              password=password,
                              host='localhost')


class BaseModel(Model):
    class Meta:
        database = dbhandle


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


class BaseModel_city(Model):
    class Meta:
        database = dbhandle_city


class City(BaseModel_city):
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
