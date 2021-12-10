import telebot
from telebot import types
from config import fullSchedule

# creating
TOKEN = "5055036871:AAEegE32QePaRBGON37ToMmLysCAwKr7RXE"
bot = telebot.TeleBot(TOKEN)


# creating buttons
@bot.message_handler(commands=['start'])
def welcome(message):
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEDc_Fhsy3I0REs2dSyR5HkYnlBUDqmrgACWgIAAsoDBgvLrSiunh-styME')

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_help = types.KeyboardButton("Начать")
    button_start = types.KeyboardButton("Помощь")

    markup.add(button_help, button_start)

    # sending message
    bot.send_message(message.chat.id,
                     "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, бот который поможет тебе не опаздывать на пары.".format(
                         message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)


# getting messages and replying them
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "Начать":
        bot.send_message(message.chat.id,
                         "Введите номер группы:")
        bot.register_next_step_handler(message, group_number)
    elif message.text == "Помощь":
        bot.send_message(message.chat.id,
                         "Просто введите номер группы и день недели.")


def group_number(message):
    global groupNumber
    groupNumber = message.text
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_monday = types.KeyboardButton("Понедельник")
    button_tuesday = types.KeyboardButton("Вторник")
    button_wednesday = types.KeyboardButton("Среда")
    button_thursday = types.KeyboardButton("Четверг")
    button_friday = types.KeyboardButton("Пятница")
    button_saturday = types.KeyboardButton("Суббота")
    button_sunday = types.KeyboardButton("Воскресение")

    markup.add(button_monday, button_tuesday, button_wednesday, button_thursday, button_friday, button_saturday,
               button_sunday)

    bot.send_message(message.chat.id,
                     "Введите день недели:", parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(message, data)


def data(message):
    global week_day
    week_day = message.text
    shed = fullSchedule(groupNumber.lower(), week_day.lower())
    if shed != "":
        bot.send_message(message.chat.id, shed)
    else:
        bot.send_message(message.chat.id, "Сегодня нет пар.")


# checking if messages were sent to bot
bot.polling(none_stop=True, interval=0)
