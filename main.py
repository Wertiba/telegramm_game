#import modules
import random
import telebot
import pymysql

from telebot import types
from icecream import ic
from messages import All_messages as messages
from config import *

#create bot and my user id
my_user_id = my_user_id
bot = telebot.TeleBot(bot_token)
#disable ic
ic.disable()


#connection to mysql db
try:
    connection = pymysql.connect(
        host=host,
        port=port,
        user=user_,
        password=password,
        database=db_name,
        cursorclass=pymysql.cursors.DictCursor
    )
    print('connection successful')
except Exception as ex:
    print(ex)
    bot.send_message(my_user_id, str(ex))

# creating table with users
# with connection.cursor() as cursor:
#    create_table_query = "CREATE TABLE users (id int AUTO_INCREMENT," \
#                         " name varchar(32)," \
#                         " ip varchar(32), PRIMARY KEY (id));"
#    cursor.execute(create_table_query)
#    print('table created successful')

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


#create player's class
class User():
    def __init__(self, name, ip, is_already_reg, race, power, health):
        self.name = name
        self.ip = ip
        self.is_already_reg = is_already_reg
        self.race = race
        self.power = power
        self.health = health

user = User(None, None, None, None, None, None)


#create races objects
vikings = Races('викинги', 'vikings', 'just_number', '650', '450')
peoples = Races('современники', 'peoples', 'just_number', '800', '300')
nigers = Races('негры', 'nigers', 'just_number', '600', '800')
polars = Races('полярники', 'polars', 'just_number', '600', '600')
fire_regiments = Races('огнеполки', 'fire_regiments', 'just_number', '850', '200')

#create enemies objects
human = Enemy('человек', '400', '300')
orc = Enemy('орк', '150', '800')
undead = Enemy('нежить', '600', '200')
elf = Enemy('эльф', '400', '100')

#list with all objects
list_races = [vikings, peoples, nigers, polars, fire_regiments]
list_enemies = [human, orc, undead, elf]


#function for select all
def select_all(cursor):
    ic.enable()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    print('\nObjects in db:')
    for row in rows:
        ic(row)
    ic.disable()


#function for select user's ip
def select_ip(message):
    try:
        with connection.cursor() as cursor:
            select_query = f"SELECT * FROM users WHERE ip = {str(message.chat.id)}"
            cursor.execute(select_query)
            rows = cursor.fetchall()

            print('selected successful')
            quantity_rows = len(rows)

            #insert query
            if quantity_rows == 0:
                insert_query = f"INSERT INTO users (name, ip) VALUES ('{user.name}', '{str(message.chat.id)}');"
                cursor.execute(insert_query)
                connection.commit()
                print('insert was successful')

            select_all(cursor)

    #sending exception for me
    except Exception as ex:
        print(ex)
        bot.send_message(my_user_id, str(ex))

    finally:
        connection.close()

def choise_race_markup(message):
    #add player's object
    global user
    user.name = str(message.chat.first_name).lower()
    user.ip = message.chat.id


    #markup
    murkup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(vikings.name, callback_data='choose_vikings')
    btn2 = types.InlineKeyboardButton(peoples.name, callback_data='choose_peoples')
    btn3 = types.InlineKeyboardButton(nigers.name, callback_data='choose_nigers')
    btn4 = types.InlineKeyboardButton(polars.name, callback_data='choose_polars')
    btn5 = types.InlineKeyboardButton(fire_regiments.name, callback_data='choose_fire_regiments')

    murkup.row(btn1, btn2)
    murkup.row(btn3, btn4)
    murkup.row(btn5)

    bot.send_message(message.chat.id, 'Ок, выбирай рассу)', reply_markup=murkup)
    bot.register_next_step_handler(message, callback_query)


#functional for callback for choose race
def choose_race_functional(data, message):
    global user

    if str(data) == 'choose_fire_regiments':
        user_race = 'fire_regiments'
    else:
        user_race = str(data).split('_')[1]


    for race in list_races:
        if race.title == user_race:
            user.race = race.title
            user.health = race.health
            user.power = race.power


            bot.send_message(message.chat.id, messages['choose_rase'])


    print(user.race, user.power, user.name, user.health, user.is_already_reg, user.ip )


def action_functional(data, message):
    pass









@bot.message_handler(commands=['action'])
def action_markup(message):
    #markup
    murkup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Вступить в бой', callback_data='action_fight')
    btn2 = types.InlineKeyboardButton('Торговать', callback_data='action_trade')
    btn3 = types.InlineKeyboardButton('Что-то ещё', callback_data='action_anything')

    murkup.row(btn1, btn2)
    murkup.row(btn3)

    bot.send_message(message.chat.id, 'Выберите действие', reply_markup=murkup)
    bot.register_next_step_handler(message, callback_query)













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

    #check ip in db
    select_ip(message)

    bot.send_message(message.chat.id, f'Приветствую тебя, {message.chat.first_name}')
    bot.send_message(message.chat.id, messages['start_message'], reply_markup=murkup)

    bot.register_next_step_handler(message, callback_query)


#callbacks
@bot.callback_query_handler(func=lambda callback: True)
def callback_query(callback):
    # print(callback)
    message = callback.message
    if callback.data == 'bot_info':
        bot.send_message(message.chat.id, 'Это информация о боте')

    elif callback.data == 'donate_me':
        bot.send_message(message.chat.id, 'Вот ссылка на донат')

    elif callback.data == 'start_game':
        choise_race_markup(message)

    elif callback.data == 'tech_help':
        bot.send_message(message.chat.id, 'Напиши на мой айди)')


    #choose race
    if 'choose_' in callback.data:
        choose_race_functional(callback.data, message)

    if 'action_' in callback.data:
        action_functional(callback.data, message)



bot.polling(none_stop=True)
