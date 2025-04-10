import telebot
from config import API_TOKEN
from handlers import *
bot = telebot.TeleBot(API_TOKEN)


if __name__ == "__main__":
    bot.polling(none_stop=True)
