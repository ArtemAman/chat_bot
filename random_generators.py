# -*- coding: utf-8 -*-
import string
import random
from random import randint
from settings import airport_generation_json


def gate_generator():
    rows = ['A', 'B', 'C', 'D', 'E', 'F']
    row = random.choice(rows)
    seat = randint(1, 50)
    gate = row + str(seat)
    return gate


def random_seat_generator():
    rows = ['A', 'B', 'C', 'D', 'E', 'F']
    row = random.choice(rows)
    seat = randint(1, 34)
    final_seat = str(seat) + row
    return final_seat


def random_flight_generator():
    a = string.ascii_uppercase
    letter_1 = random.choice(a)
    letter_2 = random.choice(a) + ' '
    number = randint(1111, 9999)
    flight = letter_1 + letter_2 + str(number)
    return flight


def airport_generator(city):
    a = random.choice(airport_generation_json[city]['airport'])
    airport = ' (' + a + ')'
    return airport



