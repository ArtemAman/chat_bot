# -*- coding: utf-8 -*-


import datetime
from pprint import pprint
import random

from pony.orm import db_session

from databse_usage import Timetable
from settings import cities_of_arrival, airlines

sundays = []
tuesdays = []
fridays = []
date_31 = []
date_20 = []


def every_date(date_to_fly, list_to_append):
    now = datetime.datetime.now()
    searched_day = now
    after_a_year = now + datetime.timedelta(days=365)
    while searched_day < after_a_year:
        while searched_day.day != date_to_fly:
            searched_day = searched_day + datetime.timedelta(days=1)
        list_to_append.append(searched_day.strftime("%d-%m-%Y"))
        searched_day = searched_day + datetime.timedelta(days=1)
        continue


def every_weekday(weekday, list_to_append):
    now = datetime.datetime.now()
    searched_day = now
    after_a_year = now + datetime.timedelta(days=365)
    while searched_day < after_a_year:
        while searched_day.isoweekday() != weekday:
            searched_day = searched_day + datetime.timedelta(days=1)
        list_to_append.append(searched_day.strftime("%d-%m-%Y"))
        searched_day = searched_day + datetime.timedelta(days=1)
        continue


def destinations(city, timetable_list):
    if city in cities_of_arrival:
        correct_time_list = []
        for elem in timetable_list:
            rand_time = ''.join(
                f'{"{0:0=2d}".format(random.randrange(1, 23, 1))}.{"{0:0=2d}".format(random.randrange(1, 59, 1))}')
            correct_time = ''.join(f'{elem} {rand_time} {random.choice(airlines)}')
            correct_time_list.append(correct_time)
        return correct_time_list


def dispatcher(city_of_arrival):
    if city_of_arrival == 'London':
        every_date(20, date_20)
        direction = destinations(city=city_of_arrival, timetable_list=date_20)
        return direction
    elif city_of_arrival == 'Berlin':
        every_date(31, date_31)
        direction = destinations(city=city_of_arrival, timetable_list=date_31)
        return direction
    elif city_of_arrival == 'Paris':
        every_weekday(2, tuesdays)
        direction = destinations(city=city_of_arrival, timetable_list=tuesdays)
        return direction
    elif city_of_arrival == 'Moscow':
        every_weekday(5, fridays)
        direction = destinations(city=city_of_arrival, timetable_list=fridays)
        return direction
    elif city_of_arrival == 'NewYork':
        every_weekday(7, sundays)
        direction = destinations(city=city_of_arrival, timetable_list=sundays)
        return direction


def dispatcher_run():
    timetable_json = {}

    for item in cities_of_arrival:
        city_of_departure = item
        new_cities_list = cities_of_arrival.copy()
        new_cities_list.remove(item)
        timetable_dict = {}
        for item_2 in new_cities_list:
            city_of_arrival = item_2
            timetable_local = dispatcher(city_of_arrival=city_of_arrival, )
            timetable_dict[city_of_arrival] = timetable_local

        timetable_json[city_of_departure] = timetable_dict

    return timetable_json


@db_session
def base_maker():
    if not Timetable.exists():
        timetable = dispatcher_run()
        for departure_city, arrival_city_key in timetable.items():
            for arrival_city, flights in arrival_city_key.items():
                for flight in flights:
                    Timetable(departure_city=departure_city,
                              destination_city=arrival_city,
                              flight=flight)
    else:
        print('ololo')


if __name__ == '__main__':
    # base_maker()
    a = dispatcher_run()
    pprint(a)

# a = dispatcher(city_of_departure='London', city_of_arrival='Berlin', date='20-09-2020')
# print(a)
