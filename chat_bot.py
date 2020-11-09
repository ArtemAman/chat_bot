# -*- coding: utf-8 -*-


import logging
from datetime import datetime

import requests
import vk_api
from pony.orm import db_session
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

import handlers
from _Token import TOKEN
from databse_usage import UserState, Registration, Timetable
from settings import GROUP_ID
from vk_api.utils import get_random_id
import settings
from dispatcher import base_maker

log = logging.getLogger('bot')


def logging_conf():
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
    stream_handler.setLevel(logging.DEBUG)

    file_handler = logging.FileHandler(filename='bot_log')
    file_handler.setFormatter(logging.Formatter('%(asctime)s %(message)s'))
    file_handler.setLevel(logging.DEBUG)

    log.addHandler(stream_handler)
    log.addHandler(file_handler)
    log.setLevel(logging.DEBUG)


class Bot:
    """
    Echo bot для вконтакте
    Use python 3.7
    """

    def __init__(self, group_id, token):
        """

        :param group_id: id из группы  в вк
        :param token: секретный токен для вышеупомянутой группы
        """
        self.group_id = group_id
        self.token = token
        self.vk = vk_api.VkApi(token=token)
        self.long_poller = VkBotLongPoll(vk=self.vk, group_id=self.group_id)
        self.api = self.vk.get_api()
        self.flights = []

    def run(self):

        """

        запуск бота
        """

        for event in self.long_poller.listen():
            log.info('Получено новое событие')
            try:
                self.on_event(event=event)
            except Exception as err:
                log.exception(f'ошибка в обработке события {err}')
                continue

    @db_session
    def on_event(self, event):
        """
        отправляет определенные сообщения пользователю
        :param event:
        :return:
        """
        if event.type != VkBotEventType.MESSAGE_NEW:
            log.debug('мы пока не умеем обрабатывать события такого типа %s', event.type)
            return
        user_id = event.object.peer_id
        text = event.object.text

        state = UserState.get(user_id=user_id)

        if state is not None:
            self.continue_scenario(text=text, state=state, user_id=user_id)
            # continue scenario
        else:
            for intent in settings.INTENTS:
                if any(token in text for token in intent['tokens']):
                    if intent['answer']:
                        self.send_text(intent['answer'], user_id)
                    else:
                        self.start_scenario(intent['scenario'], user_id=user_id, text=text)
                    break
            else:
                self.send_text(settings.DEFAULT_ANSWER, user_id)

    def send_text(self, text_to_send, user_id):
        self.api.messages.send(message=text_to_send,
                               random_id=get_random_id(),
                               peer_id=user_id
                               )

    def send_img(self, img, user_id):
        upload_url = self.api.photos.getMessagesUploadServer()['upload_url']
        upload_data = requests.post(url=upload_url, files={'photo': ('img.png', img, 'img/png')}).json()
        images_data = self.api.photos.saveMessagesPhoto(**upload_data)
        owner_id = images_data[0]['owner_id']
        media_id = images_data[0]['id']
        attachment = f'photo{owner_id}_{media_id}'

        self.api.messages.send(attachment=attachment,
                               random_id=get_random_id(),
                               peer_id=user_id
                               )

    def send_step(self, step, user_id, text, context):
        if 'text' in step:
            self.send_text(step['text'].format(**context), user_id)
        if 'image' in step:
            handler = getattr(handlers, step['image'])
            image = handler(text, context)
            self.send_img(image, user_id)

    def start_scenario(self, scenario_name, user_id, text):
        scenario = settings.SCENARIOS[scenario_name]
        first_step = scenario['first_step']
        step = scenario['steps'][first_step]
        self.send_step(step, user_id, text, context={})
        UserState(user_id=user_id, scenario_name=scenario_name, step_name=first_step, context={})

    def continue_scenario(self, text, state, user_id):
        steps = settings.SCENARIOS[state.scenario_name]['steps']
        step = steps[state.step_name]
        handler = getattr(handlers, step['handler'])
        if handler(text=text, context=state.context):
            # next step
            if step['next_step'] == 'step4':
                self.flights = []
                received_timetable = list(Timetable.select(lambda timetable: timetable.departure_city == state.context[
                    'departure_city'] and timetable.destination_city == state.context['destination_city']))

                for item in received_timetable:
                    string = item.flight
                    date = string.split(' ')[0]
                    if datetime.strptime(date, "%d-%m-%Y") > datetime.strptime(state.context['user_date'], "%d-%m-%Y"):
                        flight_element = '{0}-{1} {2}'.format(item.departure_city, item.destination_city,
                                                              item.flight)
                        self.flights.append(flight_element)
                norm_flights = '\n'.join(self.flights[:5])
                state.context['flight'] = norm_flights
            if step['next_step'] == 'step8':
                state.context['correct_flight'] = self.flights[state.context['correct_choice']]
            if step['next_step'] == 'step9':
                if state.context['yes_no'] == 'no':
                    state.delete()
                    text_to_send = step['failure_text2']
                    self.send_text(text_to_send, user_id)

            next_step = steps[step['next_step']]
            self.send_step(next_step, user_id, text, state.context)
            if next_step['next_step']:
                state.step_name = step['next_step']
            else:
                Registration(departure_city=state.context['departure_city'],
                             destination_city=state.context['destination_city'],
                             correct_flight=state.context['correct_flight'],
                             name=state.context['name'],
                             surname=state.context['surname'],
                             phone_number=state.context['phone_number'],
                             comment=state.context['comment'])
                state.delete()
        else:
            text_to_send = step['failure_text']
            self.send_text(text_to_send, user_id)


if __name__ == '__main__':
    logging_conf()
    bot_1 = Bot(group_id=GROUP_ID, token=TOKEN)
    base_maker()
    bot_1.run()
