#import modules
import random
import telebot

from telebot import types
from icecream import ic
from messeges import All_messeges as messages

#create bot and my user id
my_user_id = 5900045265
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
#delete reply markup: murkup = types.ReplyKeyboardRemove()
@bot.message_handler(commands=['start'])
def start(message):
    murkup = types.InlineKeyboardMarkup

    bot.send_message(message.chat.id, messages['start_message'])







bot.polling(none_stop=True)