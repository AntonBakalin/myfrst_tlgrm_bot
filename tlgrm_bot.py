# -*- coding: utf-8 -*-

import time
import telebot
import threading
import BotLib as bl
import os

os.chdir('./myfrst_tlgrm_bot')

with open('key.txt', 'r', encoding='utf-8') as key_file:
    token = key_file.read()

bot = telebot.TeleBot(token)
print(token)


@bot.message_handler(commands=['start'])
def start(message):
    user = message.chat.id
    users = bl.readUsers()['users']
    if str(user) not in users:
        bl.addUser(user)
        bot.send_message(user, 'Вы подписались на рассылку информации!')
    else:
        bot.send_message(user, 'Вы уже подписаны!')


@bot.message_handler(commands=['stop'])
def stop(message):
    user = message.chat.id
    users = bl.readUsers()['users']
    if str(user) in users:
        bl.delUser(user)
        bot.send_message(user, 'Вы отписались от рассылки информации!')
    else:
        bot.send_message(user, 'Вы не были подписаны!')


@bot.message_handler(commands=['check'])
def check(message):
    user = message.chat.id
    user_name = message.from_user.username
    users = bl.readUsers()['users']
    if str(user) in users:
        urls = bl.getURLlist()
        lots = bl.getLots(urls)
        lots_data = bl.checkDiff(lots)
        if lots_data:
            bot.send_message(user
                             , 'Появились новые торги!\n' + lots_data
                             , parse_mode="Markdown")
            bl.storeData(lots)
            for another_user in users:
                if another_user != str(user):
                    out_msg = 'Появились новые торги!\nСкажи спасибо, ' + user_name + '\n'
                    bot.send_message(another_user, out_msg + lots_data, parse_mode="Markdown")

        else:
            bot.send_message(user, 'Обновлений нет! (((\nПосмотреть текущие /current')
    else:
        bot.send_message(user, 'Вы не подписаны!')


@bot.message_handler(commands=['help'])
def rethelp(message):
    user = message.chat.id
    answer = '''Бот автоматически проверяет наличие закупок по ключевым словам на площадке [Госзакупки](https://zakupki.gov.ru/).
Ключевые слова зашиты в код для экономии времени.
Команды:
/start - Подписаться на обновления торгов.
/stop - Отписаться от рассылки.
/check - Принудительно проверить наличие новых торгов. Остальные пользователи получат уведомление.
/current - Вывести список сохраненных торгов.
'''
    bot.send_message(user, answer, parse_mode="Markdown")


@bot.message_handler(commands=['current'])
def cur(message):
    user = message.chat.id
    users = bl.readUsers()['users']
    if str(user) in users:
        outmessage = bl.retDataFromStorage()
        bot.send_message(user
                         , 'Список торгов\n' + outmessage
                         , parse_mode="Markdown")
    else:
        bot.send_message(user, 'Вы не подписаны!')

def Checker():
    while True:
        users = bl.readUsers()['users']
        urls = bl.getURLlist()
        lots = bl.getLots(urls)
        lots_data = bl.checkDiff(lots)
        if users:
            print(users)
            if lots_data:
                for user in users:
                    out_msg = 'Появились новые торги!\nСкажи спасибо, Боту!\n'
                    bot.send_message(user, out_msg + lots_data, parse_mode="Markdown")
            bl.storeData(lots)
            time.sleep(8200)

def Polling():
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            pass

threadChecker = threading.Thread(target = Checker)
threadPolling = threading.Thread(target = Polling)
threadChecker.start()
threadPolling.start()


