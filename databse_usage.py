# -*- coding: utf-8 -*-

from pony.orm import Database, Required, Json
from settings import DB_CONFIG

db = Database()
db.bind(**DB_CONFIG)


class UserState(db.Entity):
    """Состояние пользователя при покупке билетов"""
    user_id = Required(int, unique=True)
    scenario_name = Required(str)
    step_name = Required(str)
    context = Required(Json)


class Registration(db.Entity):
    """Данные о выборе рейса"""
    departure_city = Required(str)
    destination_city = Required(str)
    correct_flight = Required(str)
    name = Required(str)
    surname = Required(str)
    comment = Required(str)
    phone_number = Required(str)


class Timetable(db.Entity):
    """Таблица для хранения расписания"""
    departure_city = Required(str)
    destination_city = Required(str)
    flight = Required(str)


db.generate_mapping(create_tables=True)
