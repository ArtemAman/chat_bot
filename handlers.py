import re

from settings import cities_of_arrival, cities_of_departure, param_ch_img, font_header, font_main, font_bold, base_img
from datetime import datetime

from ticket_maker import ticket_changer

re_city = r'[a-zA-Z]{1,40}'
re_date = r'(^\d{2}-\d{2}-\d{4}$)'
re_choice = r'(^[1-5]$)'
re_name = r'(^([А-Я]{1}[а-яё]{1,23}|[A-Z]{1}[a-z]{1,23})$)'
re_phone_number = r'^((8|\+7)[\- ]?)?(\(?\d{3}\)?[\- ]?)?[\d\- ]{7,10}$'


def handler_city_departure(text, context):
    if text in cities_of_departure:
        context['departure_city'] = text
        return True
    else:
        return False


def handler_city_destination(text, context):
    if text in cities_of_arrival:
        if context['departure_city'] != text:
            context['destination_city'] = text
            return True
    else:
        return False


def handler_date(text, context):
    match = re.match(re_date, text)
    if match:
        if datetime.strptime(text, "%d-%m-%Y") > datetime.today():
            context['user_date'] = text
            return True
    else:
        return False


def handler_correct_choice(text, context):
    match = re.match(re_choice, text)
    if match:
        context['correct_choice'] = int(text) - 1
        return True
    else:
        return False


def handler_name(text, context):
    match = re.match(re_name, text)
    if match:
        context['name'] = text
        return True
    else:
        return False


def handler_surname(text, context):
    match = re.match(re_name, text)
    if match:
        context['surname'] = text
        return True
    else:
        return False


def handler_yes_no(text, context):
    if text == 'yes':
        context['yes_no'] = text
        return True
    elif text == 'no':
        context['yes_no'] = text
        return True
    else:
        return False


def comment_handler(text, context):
    if type(text) == str:
        context['comment'] = text
        return True
    else:
        return False


def handler_phone_number(text, context):
    match = re.match(re_phone_number, text)
    if match:
        context['phone_number'] = text
        return True
    else:
        return False


def ticket_generate_handler(text, context):
    correct_split = context['correct_flight'].split(' ')
    correct_airline = correct_split[3]

    ticket_ready_to_send = ticket_changer(base_img=base_img, paste_img=param_ch_img[correct_airline]['img'],
                                          header_color=param_ch_img[correct_airline]['color'],
                                          font_header=font_header, font_main=font_main, font_bold=font_bold,
                                          passenger_info=context)
    return ticket_ready_to_send
