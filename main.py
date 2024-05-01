#import modules
import random
import telebot

from telebot import types
from icecream import ic

#create bot
bot = telebot.TeleBot('7177989754:AAFO8VfvNuLfa7hVyszlwZjz6UEL-kJ6I_s')
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


vikings = Races('викинги', 'just_title', 'just_number', '650', '450')
peoples = Races('современники', 'just_title', 'just_number', '800', '300')
nigers = Races('негры', 'just_title', 'just_number', '600', '800')
polars = Races('полярники', 'just_title', 'just_number', '600', '600')
fire_regiments = Races('огнеполки', 'just_title', 'just_number', '850', '200')

#list with all races
races_list = [vikings, peoples, nigers, polars, fire_regiments]

#function for command start
@bot.message_handler(commands=['start'])
def start(message):
    murkup = types.ReplyKeyboardMarkup()
    btn1 = types.KeyboardButton('x')
    btn2 = types.KeyboardButton('y')
    murkup.row(btn1, btn2)

    bot.send_message(message.chat.id, f'Здравствуйте, {message.from_user.first_name}', reply_markup=murkup)

bot.polling(none_stop=True)