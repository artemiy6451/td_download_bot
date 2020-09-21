import telebot
import requests
from bs4 import BeautifulSoup
import os
import time

token = '1157438899:AAGO5VIRkmrT--2-aDDPVIk3DThtE-rr3Og'
song_name = ''

bot = telebot.TeleBot(token)
keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row('/start')


while True:
    try:

        @bot.message_handler(commands=['start'])
        def start_message(message):
            bot.send_message(message.chat.id, 'Отправь мне название трека', reply_markup=keyboard1)

        @bot.message_handler(content_types=['text'])
        def send_aud(message):
            global song_name
            req = requests.get('https://zaycev.net/search.html?query_search=' + message.text)
            if req.status_code == 200:
                soup = BeautifulSoup(req.text, 'html.parser')
                link = soup.find('a', class_='musicset-track__download-link')
                print(link.get('title').replace('Скачать трек ', ''))
                song_name = link.get('title').replace('Скачать трек ', '')
                req = requests.get('https://zaycev.net' + str(link.get('href')))
                with open(f"{link.get('title').replace('Скачать трек ', '')}.mp3", 'wb') as f:
                    f.write(req.content)
                    bot.send_audio(message.chat.id, audio=open(f'{song_name}.mp3', 'rb'))
                os.remove(f'{song_name}.mp3')

        bot.polling()
    except Exception:

        time.sleep(10)
        print(Exception)