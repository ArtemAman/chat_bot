# -*- coding: utf-8 -*-
from copy import deepcopy
import datetime
from unittest import TestCase
from unittest.mock import patch, Mock
from pony.orm import db_session, rollback
from vk_api.bot_longpoll import VkBotMessageEvent
from databse_usage import  Timetable
import settings
from chat_bot import Bot


def isolate_db(test_func):
    def wrapper(*args, **kwargs):
        with db_session:
            test_func(*args, **kwargs)
            rollback()
    return wrapper



@db_session
def get_base_timetable():
    flights = []
    received_timetable = list(Timetable.select(lambda timetable: timetable.id <= 53))
    date = datetime.datetime.now() + datetime.timedelta(days=30)
    for item in received_timetable:
        string = item.flight
        date_of_timetable = string.split(' ')[0]
        if date < datetime.datetime.strptime(date_of_timetable, "%d-%m-%Y"):
            flight_element = ('{0}-{1} {2}').format(item.departure_city, item.destination_city,
                                                item.flight)
            flights.append(flight_element)
    norm_flights = '\n'.join(flights[:5])

    # print(norm_flights)

    return norm_flights


get_base_timetable()


class Test1(TestCase):
    RAW_EVENT = {'type': 'message_new',
                 'object': {'date': 1592499781, 'from_id': 599467213, 'id': 242, 'out': 0, 'peer_id': 599467213,
                            'text': 'привет', 'conversation_message_id': 242, 'fwd_messages': [], 'important': False,
                            'random_id': 0, 'attachments': [], 'is_hidden': False},
                 'group_id': 195814223,
                 'event_id': '275d2158bacfa378b495fe088703150142b41ca6'}

    def test_run(self):
        count = 5
        obj = {'a': 1}
        events = [obj] * count
        long_poller_mock = Mock(return_value=events)
        long_poller_listen_mock = Mock()
        long_poller_listen_mock.listen = long_poller_mock

        with patch('chat_bot.vk_api.VkApi'):
            with patch('chat_bot.VkBotLongPoll', return_value=long_poller_listen_mock):
                bot = Bot('', '')
                bot.on_event = Mock()
                bot.run()

                bot.on_event.assert_called()
                bot.on_event.assert_any_call(event=obj)
                assert bot.on_event.call_count == count

    future_date = datetime.datetime.now() + datetime.timedelta(days=30)
    date_str = datetime.datetime.strftime(future_date, "%d-%m-%Y")

    INPUTS = ['sdfghdfsg',
              '/ticket',
              'London',
              'Paris',
              date_str,
              '1',
              'Ivanov',
              'Ivan',
              'fsdfsdfsd',
              'yes',
              '899980066666',
              ]

    flight = get_base_timetable()

    EXPECTED_OUTPUTS = [
        settings.DEFAULT_ANSWER,
        settings.SCENARIOS['purchase']['steps']['step1']['text'],
        settings.SCENARIOS['purchase']['steps']['step2']['text'],
        settings.SCENARIOS['purchase']['steps']['step3']['text'],
        settings.SCENARIOS['purchase']['steps']['step4']['text'].format(flight=flight),
        settings.SCENARIOS['purchase']['steps']['step5']['text'],
        settings.SCENARIOS['purchase']['steps']['step6']['text'],
        settings.SCENARIOS['purchase']['steps']['step7']['text'],
        settings.SCENARIOS['purchase']['steps']['step8']['text'].format(correct_flight=flight.split('\n')[0],
                                                                        surname='Ivanov', name='Ivan'),
        settings.SCENARIOS['purchase']['steps']['step9']['text'],
        settings.SCENARIOS['purchase']['steps']['step10']['text'].format(phone_number='899980066666')

    ]

    @isolate_db
    def test_run_2(self):
        send_mock = Mock()
        api_mock = Mock()
        api_mock.messages.send = send_mock

        events = []
        for input_text in self.INPUTS:
            event = deepcopy(self.RAW_EVENT)
            event['object']['text'] = input_text
            events.append(VkBotMessageEvent(event))

        long_poller_mock = Mock()
        long_poller_mock.listen = Mock(return_value=events)

        with patch('chat_bot.VkBotLongPoll', return_value=long_poller_mock):
            bot = Bot('', '')
            bot.api = api_mock
            bot.send_img = Mock()
            bot.run()

        assert send_mock.call_count == len(self.INPUTS)

        real_outputs = []

        for call in send_mock.call_args_list:
            args, kwargs = call
            real_outputs.append(kwargs['message'])

        # Эти принты помогут найти несоответствие в вводах/выводах
        for real, expec in zip(real_outputs, self.EXPECTED_OUTPUTS):
            print(real)
            print('-' * 50)
            print(expec)
            print('-' * 50)
            print(real == expec)
            print('_' * 50)

        assert real_outputs == self.EXPECTED_OUTPUTS
