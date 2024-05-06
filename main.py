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
        user=user,
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


#function for select all
def select_all(cursor):
    ic.enable()
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()
    print('Objects in db:\n\n')
    for row in rows:
        ic(row)
    ic.disable()


#function for select user's ip
def select_ip(message):
    print(str(message.from_user.first_name).lower())
    try:
        with connection.cursor() as cursor:
            select_query = f"SELECT * FROM users WHERE ip = {str(message.chat.id)}"
            cursor.execute(select_query)
            rows = cursor.fetchall()

            print('selected successful')
            quantity_rows = len(rows)

            #insert query
            if quantity_rows == 0:
                insert_query = f"INSERT INTO users (name, ip) VALUES ('{str(message.from_user.first_name).lower()}', '{str(message.chat.id)}');"
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

def choise_race(message):
    murkup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton(vikings.name, callback_data='choose_vikings')
    btn2 = types.InlineKeyboardButton(peoples.name, callback_data='choose_vikings')
    btn3 = types.InlineKeyboardButton(nigers.name, callback_data='choose_vikings')
    btn4 = types.InlineKeyboardButton(polars.name, callback_data='choose_vikings')
    btn5 = types.InlineKeyboardButton(fire_regiments.name, callback_data='choose_vikings')

    murkup.row(btn1, btn2)
    murkup.row(btn3, btn4)
    murkup.row(btn5)

    bot.send_message(message.chat.id, 'Ок, выбирай рассу)', reply_markup=murkup)
















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
        choise_race(message)

    elif callback.data == 'tech_help':
        bot.send_message(message.chat.id, 'Напиши на мой айди)')




bot.polling(none_stop=True)
