from bot import bot
from telebot import types
from api.codewars_api import get_user_info
from api.hackerrank_api import get_info_about_user


states_users = {}

@bot.message_handler(commands=["start"])
def say_hello(message):
    bot.send_message(message.chat.id, "Привет!")

@bot.message_handler(commands=["help"])
def get_help(message):
    bot.send_message(message.chat.id, "/start - приветствие,\n /help - помощь, \n /codewars - получить статистику пользователя codewars")



@bot.message_handler(commands=["get_statistic"])
def button_message(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_cdw=types.KeyboardButton("Codewars")
    item_hkr=types.KeyboardButton("HackerRank")
    markup.add(item_cdw, item_hkr)
    bot.send_message(message.chat.id, "Выберите что вам нужно...", reply_markup=markup)

@bot.message_handler(content_types="text")
def message_reply(message):
    user_id = message.chat.id

    if user_id in states_users:
        if states_users[user_id] == "awaiting_username":
            username = message.text
            user_statistic = get_user_info(username)
            rank_name = user_statistic.get('ranks', {}).get('overall', {}).get('name')
            total = user_statistic.get('codeChallenges', {}).get("totalCompleted")



            bot.send_message(user_id, f"Получена статистика для пользователя: \n Юзернейм: {username}\n Ранг: {rank_name}\n Всего решено задач: {total}")

            del states_users[user_id]
            return


    if message.text == "Codewars":
        bot.send_message(message.chat.id,"Введите имя пользователя для получения статистики:")

        states_users[user_id] = "awaiting_username"


# @bot.message_handler(commands=["/help"])
# def help_user(message):
#     bot.send_message(message.chat.id, "/start -  приветствие,\n /help - помощь, \n /codewars - получить статистику пользователя codewars")


bot.infinity_polling()


