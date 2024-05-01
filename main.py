#import modules
import random
import telebot

from telebot import types
from icecream import ic

#create bot
bot = telebot.TeleBot('6042698676:AAEfUDOR2v2KqOkxRfpC6s1qn6hYpoU7Pdk')
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

races_list = [vikings, peoples, nigers, polars, fire_regiments]
