from datetime import datetime, timedelta
from io import BytesIO

from PIL import ImageDraw, Image, ImageFont
from random_generators import gate_generator, random_flight_generator, random_seat_generator, airport_generator
from settings import param_ch_img, font_header, font_main, font_bold, base_img


def ticket_changer(base_img, paste_img, header_color, font_header, font_main, font_bold, passenger_info):
    # я понимаю, что делать функцию с таким колличеством параметров это не есть хорошо, но неужели лучше принять
    # всю инфу каким нибудь одним параметром и делить потом ее внутри функции?
    # TODO Вообще да, было бы удобно собрать данные по группам хотя бы
    # TODO например передавать сюда словарь "данные_о_пассажире", который бы хранил всю информацию,
    # TODO которая надо разместить на билете
    # TODO А какие-то системные параметры вроде base_img, paste_img, header_color, font_header
    # TODO можно оставить и так.
    base = Image.open(base_img).convert("RGBA")
    paste = Image.open(paste_img).convert("RGBA")
    fnt = ImageFont.truetype(font_main, 30)
    font_bold = ImageFont.truetype(font_bold, 30)
    fnt_small = ImageFont.truetype(font_main, 20)
    fnt_small_2 = ImageFont.truetype(font_main, 13)
    fnt2 = ImageFont.truetype(font_header, 30)
    draw = ImageDraw.Draw(base)

    seat = random_seat_generator()
    gate = gate_generator()
    flight = random_flight_generator()

    correct_split = passenger_info['correct_flight'].split(' ')
    correct_time = correct_split[2].replace('.', ':')
    correct_date = correct_split[1]
    boarding = datetime.strptime(correct_time, "%H:%M") - timedelta(minutes=40)
    boarding_str = boarding.strftime("%H:%M")
    end_of_boarding = datetime.strptime(correct_time, "%H:%M") - timedelta(minutes=20)
    end_of_boarding_str = end_of_boarding.strftime("%H:%M")
    passenger = passenger_info['name'] + ' ' + passenger_info['surname']
    departure = passenger_info['departure_city'] + airport_generator(passenger_info['departure_city'])
    arrival = passenger_info['destination_city'] + airport_generator(passenger_info['destination_city'])

    draw.polygon(((0, 0), (1009, 0), (1009, 81), (0, 81)), outline=header_color, fill=header_color)
    base.paste(paste, (0, 0))
    base.paste(paste, (743, 0))

    txt = Image.new("RGBA", base.size, (255, 255, 255, 0))
    d = ImageDraw.Draw(txt)

    d.text((250, 25), 'Посадочный талон', font=font_bold, fill=(0, 0, 0, 240))
    d.text((550, 29), 'Boarding pass', font=fnt2, fill=(0, 0, 0, 240))

    d.text((108, 132), gate, font=fnt, fill=(0, 0, 0, 240))
    d.text((108, 210), boarding_str, font=fnt, fill=(0, 0, 0, 240))
    d.text((108, 300), end_of_boarding_str, font=fnt, fill=(0, 0, 0, 240))
    d.text((332, 125), passenger, font=fnt_small, fill=(0, 0, 0, 240))
    d.text((332, 187), departure, font=fnt_small, fill=(0, 0, 0, 240))
    d.text((535, 187), arrival, font=fnt_small, fill=(0, 0, 0, 240))
    d.text((332, 250), correct_date, font=fnt_small, fill=(0, 0, 0, 240))
    d.text((535, 250), correct_time, font=fnt_small, fill=(0, 0, 0, 240))
    d.text((332, 310), seat, font=fnt, fill=(0, 0, 0, 240))
    d.text((535, 310), flight, font=fnt, fill=(0, 0, 0, 240))

    d.text((782, 125), passenger, font=fnt_small_2, fill=(0, 0, 0, 240))
    d.text((782, 187), correct_time, font=fnt_small_2, fill=(0, 0, 0, 240))
    d.text((782, 250), flight, font=fnt_small_2, fill=(0, 0, 0, 240))
    d.text((782, 310), seat, font=fnt_small, fill=(0, 0, 0, 240))

    d.text((900, 187), correct_date, font=fnt_small_2, fill=(0, 0, 0, 240))
    d.text((900, 250), departure, font=fnt_small_2, fill=(0, 0, 0, 240))
    d.text((900, 310), arrival, font=fnt_small_2, fill=(0, 0, 0, 240))

    out = Image.alpha_composite(base, txt)
    # with open ('temp_ticket.png', 'wb') as f:
    #     out.save(f, 'png')

    temp_file = BytesIO()
    out.save(temp_file, 'png')
    temp_file.seek(0)

    return temp_file

# a = ticket_changer(base_img=base_img, paste_img=param_ch_img['Aeroflot']['img'],
#                header_color=param_ch_img['Aeroflot']['color'],
#                font_header=font_header, font_main=font_main, font_bold=font_bold, gate='C3', boarding='15.55',
#                end_of_boarding='15.55',
#                passenger='passenger', departure='departure', arrival='arrival', date='date', time='time',
#                flight='SU 2101', seat='12F')
#
#
# print(a)
