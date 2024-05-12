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
    def __init__(self, name, title, power, health, is_tradyble, reward):
        self.name = name
        self.title = title
        self.power = power
        self.health = health
        self.is_tradyble = is_tradyble
        self.reward = reward


    #fight
    def fight(self):
        ic.enable()
        ic(user.health, self.power, self.health, user.power, user.ballance)
        ic.disable()


        if (user.health - self.power) > (self.health - user.power):
            data = f'Поздравляю! Вы одержали победу!\n' \
                   f'Вы получили {self.reward}'
            user.ballance += self.reward

        elif (user.health - self.power) > (self.health - user.power):
            data = 'Вы проиграли('


        return data

    #trade
    def trade_functional(self, call):
        ic.enable()
        ic(user.health, user.power)
        data = str(call.data).split('_')[1]

        if user.ballance - 5 >= 0:
            user.ballance -= 5
            if data == 'force':
                user.power += 50

            elif data == 'hill':
                user.health += 50

            elif data == 'key':
                user.inventory.append('key')




            bot.send_message(call.message.chat.id, 'Успешно преобретено. Чтобы вернуться в деревню жмите на кнопку выше')

        else:
            bot.send_message(call.message.chat.id, 'У вас не хватает денег!')




        ic(user.health, user.power)
        ic.disable()





#create player's class
class User():
    def __init__(self, name, ip, is_already_reg, race, power, health, enemy, ballance, inventory):
        self.name = name
        self.ip = ip
        self.is_already_reg = is_already_reg
        self.race = race
        self.power = power
        self.health = health
        self.enemy = enemy
        self.ballance = ballance
        self.inventory = inventory

    #func for view inventory
    def mine_inventory(self, message):
        # markup
        murkup = types.InlineKeyboardMarkup()
        btn1 = types.InlineKeyboardButton('Отправиться в поход', callback_data='move_on')

        murkup.row(btn1)

        if len(self.inventory) == 0:
            bot.send_message(message.chat.id, 'Ваш инвентарь пуст', reply_markup=murkup)

        else:
            for i in self.inventory:
                if i == self.inventory[-1]:
                    bot.send_message(message.chat.id, f'{i}', reply_markup=murkup)

                else:
                    bot.send_message(message.chat.id, f'{i}')








user = User(None, None, None, None, None, None, None, None, [])


#create races objects
vikings = Races('викинги', 'vikings', 'just_number', 650, 450)
peoples = Races('современники', 'peoples', 'just_number', 800, 300)
nigers = Races('негры', 'nigers', 'just_number', 600, 800)
polars = Races('полярники', 'polars', 'just_number', 600, 600)
fire_regiments = Races('огнеполки', 'fire_regiments', 'just_number', 850, 200)

#create enemies objects
human = Enemy('человек', 'human', 400, 300, True, 0)
orc = Enemy('орк','orc' , 150, 800, False, 3)
undead = Enemy('нежить','undead' , 600, 200, False, 3)
elf = Enemy('эльф','elf' , 400, 100, False, 1)

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
        try:
            connection.close()
        except pymysql.err.Error:
            pass

def choise_race_markup(message):
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

    bot.send_message(message.chat.id, 'Ок, выбирай расу', reply_markup=murkup)
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
            #add attributes
            user.name = str(message.chat.first_name).lower()
            user.ip = message.chat.id
            user.race = race.title
            user.health = race.health
            user.power = race.power
            user.ballance = 10


            bot.send_message(message.chat.id, messages['choose_rase'])
            bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)
            action_markup(message)

    #print data
    ic.enable()
    ic(user.race, user.power, user.name, user.health, user.is_already_reg, user.ip )
    ic.disable()



def action_markup(message):
    global user
    #get enemy
    mob = random.choice(list_enemies)
    user.enemy = mob

    #markup
    murkup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Вступить в бой', callback_data='action_fight')
    btn2 = types.InlineKeyboardButton('Торговать', callback_data='action_trade')
    btn3 = types.InlineKeyboardButton('Пройти мимо', callback_data='action_skip')

    murkup.row(btn1, btn2)
    murkup.row(btn3)

    bot.send_message(message.chat.id, f'Вы встретили {str(mob.name).capitalize()}')
    bot.send_message(message.chat.id, 'Выберите действие', reply_markup=murkup)
    bot.register_next_step_handler(message, callback_query)


#basic function
def action_functional(data, message):
    action = str(data).split('_')[1]

    # create markup
    murkup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Идти дальше', callback_data='move_on')
    btn2 = types.InlineKeyboardButton('Вернуться в деревню', callback_data='go_home')

    murkup.row(btn1, btn2)

    if action == 'fight':
        bot.send_message(message.chat.id, str(user.enemy.fight()), reply_markup=murkup)

    elif action == 'trade':
        if user.enemy.is_tradyble == True:
            btn3 = types.InlineKeyboardButton('Купить зелье силы', callback_data='buy_force_spell')
            btn4 = types.InlineKeyboardButton('Купить зелье исцеления', callback_data='buy_hill_spell')
            btn5 = types.InlineKeyboardButton('Купить магический ключ', callback_data='buy_key_magical')
            murkup.row(btn3, btn4)
            murkup.row(btn5)

            bot.send_message(message.chat.id, f'Торговые предложения {str(user.enemy.name).capitalize()}', reply_markup=murkup)

        else:
            bot.send_message(message.chat.id, f'С этим мобом торговля невозможна', reply_markup=murkup)


    elif action == 'skip':
        action_markup(message)


    bot.clear_step_handler_by_chat_id(chat_id=message.chat.id)



#markup for mine own village
def home_markup(message):
    #markup
    murkup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton('Отправиться в поход', callback_data='move_on')
    btn2 = types.InlineKeyboardButton('Инвентарь', callback_data='mine_inventory')

    murkup.row(btn1, btn2)

    bot.send_message(message.chat.id, 'Вы вернулись в свою деревню', reply_markup=murkup)







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


#function for get enemy after the choose race
@bot.message_handler(commands=['action'])
def first_enemy(message):
    action_markup(message)

#get and print info
@bot.message_handler(commands=['info'])
def print_info(message):
    bot.send_message(message.chat.id, f'Ваше здоровье: {user.health}\n'
                                      f'Ваш урон: {user.power}\n'
                                      f'Ваш баланс: {user.ballance}')


#callbacks
@bot.callback_query_handler(func=lambda callback: True)
def callback_query(callback):
    message = callback.message
    if callback.data == 'bot_info':
        bot.send_message(message.chat.id, 'Это информация о боте')

    elif callback.data == 'donate_me':
        bot.send_message(message.chat.id, 'Вот ссылка на донат')

    elif callback.data == 'start_game':
        choise_race_markup(message)

    elif callback.data == 'tech_help':
        bot.send_message(message.chat.id, 'Напиши на мой айди)')


    elif callback.data == 'go_home':
        home_markup(callback.message)

    elif callback.data == 'move_on':
        action_markup(callback.message)

    elif callback.data == 'mine_inventory':
        user.mine_inventory(message)


    #choose race
    if 'choose_' in callback.data:
        choose_race_functional(callback.data, message)

    elif 'action_' in callback.data:
        action_functional(callback.data, message)

    elif 'buy_' in callback.data:
        user.enemy.trade_functional(callback)



bot.polling(none_stop=True)
