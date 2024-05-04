#import modules
import random
import telebot

from telebot import types
from icecream import ic
from messages import All_messages as messages
from config import All_info as config

#create bot and my user id
my_user_id = config['my_user_id']
bot = telebot.TeleBot(config['bot_token'])
#disable ic
ic.disable()

#create class for races
class Races():
    def __init__(self, name, title, number, power, health):
        self.name = name
        self.title = title
        self.number = number
        self.power = power
        self.health = health


#create class for enemies
class Enemy():
    def __init__(self, name, power, health):
        self.name = name
        self.power = power
        self.health = health







#create races objects
vikings = Races('викинги', 'just_title', 'just_number', '650', '450')
peoples = Races('современники', 'just_title', 'just_number', '800', '300')
nigers = Races('негры', 'just_title', 'just_number', '600', '800')
polars = Races('полярники', 'just_title', 'just_number', '600', '600')
fire_regiments = Races('огнеполки', 'just_title', 'just_number', '850', '200')

#create enemies objects
human = Enemy('человек', '400', '300')
orc = Enemy('орк', '150', '800')
undead = Enemy('нежить', '600', '200')
elf = Enemy('эльф', '400', '100')

#list with all objects
races_list = [vikings, peoples, nigers, polars, fire_regiments]
enemies_list = [human, orc, undead, elf]








#function for command start
#delete inline markup: murkup = types.ReplyKeyboardRemove()
@bot.message_handler(commands=['start'])
def start(message):
    #creating inline markup
    murkup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Информация', callback_data='bot_info')
    btn2 = types.InlineKeyboardButton('Поддержать создателя', callback_data='donate_me')
    btn3 = types.InlineKeyboardButton('Начать игру', callback_data='start_game')
    btn4 = types.InlineKeyboardButton('Тех.поддержка', callback_data='tech_help')

    murkup.row(btn3)
    murkup.row(btn1, btn4)
    murkup.row(btn2)

    bot.send_message(message.chat.id, f'Приветствую тебя, {message.from_user.first_name}')
    bot.send_message(message.chat.id, messages['start_message'], reply_markup=murkup)

    bot.register_next_step_handler(message, callback_query)


@bot.callback_query_handler(func=lambda callback: True)
def callback_query(callback):
    message = callback.message
    if callback.data == 'bot_info':
        bot.send_message(message.chat.id, 'Это информация о боте')

    elif callback.data == 'donate_me':
        bot.send_message(message.chat.id, 'Вот ссылка на донат')

    elif callback.data == 'start_game':
        bot.send_message(message.chat.id, 'Ок, выбирай рассу)')

    elif callback.data == 'tech_help':
        bot.send_message(message.chat.id, 'Напиши на мой айди)')




bot.polling(none_stop=True)