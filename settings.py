cities_of_departure = ['London', 'Paris', 'Moscow', 'Berlin', 'NewYork']
cities_of_arrival = ['London', 'Paris', 'Moscow', 'Berlin', 'NewYork']
airlines = ['S7', 'Lufthansa', 'FlyEmirates', 'Aeroflot', 'BritishAirways', 'UkrAvia']
cities_line_by_line = "\n".join(cities_of_departure)
airlines_line_by_line = "\n".join(airlines)

GROUP_ID = 195814223
DEFAULT_ANSWER = 'Ничего не понял, но очень интересно. Я вообще то билетами на самолет торгую. введите ' \
                 '/help для просмотра моих возможностей'
INTENTS = [
    {
        'name': 'Направления',
        'tokens': ('куда', 'откуда', 'расписание', '/directions'),
        'scenario': None,
        'answer': f'Мы осуществляем авиасообщение между городами:\n {cities_line_by_line}'
    },
    {
        'name': 'Авиакомпании',
        'tokens': ('авиа', 'компания', '/airlines'),
        'scenario': None,
        'answer': f'Мы осуществляем продажу билетов на следующие авиакомпании:\n {airlines_line_by_line}'
    },
    {
        'name': 'меню',
        'tokens': ('/help', 'помощь'),
        'scenario': None,
        'answer': 'Полезные команды:\n'
                  '/ticket - для покупки билетов\n'
                  '/directions - что бы узнать направления\n'
                  '/airlines - что бы узнать доступные авиакомпании'

    },
    {
        'name': 'Покупка билетов',
        'tokens': ('куп', '/ticket', 'бил', 'рейс', 'ближ',),
        'scenario': 'purchase',
        'answer': None
    },
]

SCENARIOS = {
    'purchase': {
        'first_step': 'step1',
        'steps': {
            'step1': {
                'text': 'Для заказа билета введите город отправления',
                'failure_text': f'Название города должно быть на английском языке. '
                                f'Вот наши основные точки вылета\n {cities_line_by_line}',
                'handler': 'handler_city_departure',
                'next_step': 'step2'
            },
            'step2': {
                'text': 'Выберете город, куда вы хотите отправиться',
                'failure_text': f'Название города должно быть на английском языке. '
                                f'Вот наши основные направления\n {cities_line_by_line}\n'
                                f'P.S. Нельзя лететь из Москвы в Москву :))',
                'handler': 'handler_city_destination',
                'next_step': 'step3'
            },
            'step3': {
                'text': 'Введите дату вылета',
                'failure_text': 'Дата вылета должна быть в формате 01-05-2019 и она не может быть в прошлом',
                'handler': 'handler_date',
                'next_step': 'step4'
            },
            'step4': {
                'text': '{flight} \n Вот ближайшие 5 рейсов. Выберите наиболее удобный для вас.',
                'failure_text': 'Для корректного выобра рейса необходимо ввести цифру (от 1 до 5), '
                                'соответствующую вашему выбору',
                'handler': 'handler_correct_choice',
                'next_step': 'step5'
            },
            'step5': {
                'text': 'Напишите вашу фамилию как в паспорте',
                'failure_text': 'Вот пример того как вы должны ввести фамилию:  Иванов или Ivanov ',
                'handler': 'handler_surname',
                'next_step': 'step6'
            },
            'step6': {
                'text': 'Напишите ваше имя как в паспорте',
                'failure_text': 'Вот пример того как вы должны ввести фамилию:  Иван или Ivan ',
                'handler': 'handler_name',
                'next_step': 'step7'
            },

            'step7': {
                'text': 'Введите комментарий в произвольной форме',
                'failure_text': '',
                'handler': 'comment_handler',
                'next_step': 'step8'
            },
            'step8': {
                'text': 'Итак, вы летите рейсом\n {correct_flight}\n '
                        'Вы бронируете билет на имя \n{surname} {name} \n'
                        'Если все верно, то напишите - yes, если есть ошибки, то напишите - no',
                'failure_text': 'Для подтверждения ввода данных напшите - yes, если есть ошибки, напишите - no',
                'failure_text2': 'Давайте попробуем еще раз. Введите /ticket для того, что бы начать выбор заново',
                'handler': 'handler_yes_no',
                'next_step': 'step9'
            },

            'step9': {
                'text': 'Введите номер телефона для связи с вами. Если что-то пойдет не так, мы вам перезвоним'
                        'Вот ваш билет. Распечатайте его и добро пожаловать на борт',
                'failure_text': 'Введите свой номер телефона формате +79261234567 , '
                                '89261234567, 79261234567, +7 926 123 45 67 , 8(926)123-45-67',
                'handler': 'handler_phone_number',
                'next_step': 'step10'
            },
            'step10': {
                'text': 'Мы вам перезвоним по номеру телефона {phone_number} если понадобится какая-либо информация\n'
                        'Вот ваш билет. Распечатайте его и добро пожаловать на борт\n'
                        'Хорошего дня',
                'image': 'ticket_generate_handler',
                'failure_text': None,
                'handler': None,
                'next_step': None
            },
        }
    }
}

DB_CONFIG = dict(
    provider='postgres',
    user='postgres',
    host='localhost',
    password='123',
    database='vk_chat_bot',
)

param_ch_img = {
    'S7': {'img': 'img_to_add/sseven.png', 'color': (0, 255, 6)},
    'Lufthansa': {'img': 'img_to_add/luft.png', 'color': (255, 179, 0)},
    'FlyEmirates': {'img': 'img_to_add/fe.png', 'color': (255, 0, 0)},
    'Aeroflot': {'img': 'img_to_add/aero.png', 'color': (255, 255, 255)},
    'BritishAirways': {'img': 'img_to_add/ba.png', 'color': (1, 68, 149)},
    'UkrAvia': {'img': 'img_to_add/uia.png', 'color': (255, 196, 0)}
}

airport_generation_json = {
    'London': {'airport': ['LHR', 'LTN', 'STN', 'LCY']},
    'Paris': {'airport': ['XEX', 'XDT', 'XTT', 'XPG']},
    'Moscow': {'airport': ['DME', 'SVO', 'VKO', 'ZIA']},
    'Berlin': {'airport': ['QPP', 'BER', 'QWC', 'QWE']},
    'NewYork': {'airport': ['NBP', 'NES', 'TSS', 'LGA']},

}

font_header = 'fonts/Myr_it.ttf'
font_main = 'fonts/Arial.ttf'
font_bold = 'fonts/Arial_bold.ttf'
base_img = 'ticket_base.jpg'
