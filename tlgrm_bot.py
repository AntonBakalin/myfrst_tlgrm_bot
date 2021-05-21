import telebot
from pprint import pprint

token = "1857806552:AAGaAv4TjI5AyAZE_2X98UDWkvruv6yKtqg"

bot = telebot.TeleBot(token=token)

@bot.message_handler(commands=['start'])
def retstart(message):
    user = message.chat.id
    bot.send_message(user, 'start message')

@bot.message_handler(commands=['help'])
def rethelp(message):
    user = message.chat.id
    bot.send_message(user, 'help message')

@bot.message_handler(commands=['anek'])
def retanek(message):
    user = message.chat.id
    bot.send_message(user, 'anek message')

@bot.message_handler(content_types=['text'])
def rettext(message):
    print(message.text)

bot.polling(none_stop=True)
