from bot import bot
from telebot import types
from api.codewars_api import get_user_info, UserNotFoundError
from api.leet_code import get_info_about_user


states_users = {}

@bot.message_handler(commands=["start"])
def say_hello(message):
    bot.send_message(message.chat.id, "Привет!")

@bot.message_handler(commands=["help"])
def get_help(message):
    bot.send_message(message.chat.id, "/start - приветствие,\n /help - помощь, \n /get_statistic - Выбрать сайт для получения статистики пользователя")



@bot.message_handler(commands=["get_statistic"])
def button_message(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item_cdw=types.KeyboardButton("Codewars")
    item_hkr=types.KeyboardButton("LeetCode")
    markup.add(item_cdw, item_hkr)
    bot.send_message(message.chat.id, "Выберите что вам нужно...", reply_markup=markup)

@bot.message_handler(content_types="text")
def message_reply(message):
    user_id = message.chat.id

    if user_id in states_users:
        if states_users[user_id] == "awaiting_username_codewars":
            try:
                username = message.text
                get_user_statistic = get_user_info(username)
                rank_name = get_user_statistic.get('ranks', {}).get('overall', {}).get('name')
                total = get_user_statistic.get('codeChallenges', {}).get("totalCompleted")
                leader_board = get_user_statistic.get('leaderboardPosition')

                bot.send_message(user_id, f"Получена статистика для пользователя: \n Юзернейм: {username}\n Ранг: {rank_name}\n Всего решено задач: {total}\n Позиция на доске лидеров: {leader_board}")
            except UserNotFoundError as e:
                bot.send_message(user_id, str(e))

            except Exception as e:
                bot.send_message(user_id, f"Произошла ошибка: {str(e)}")

            del states_users[user_id]
            return

        elif states_users[user_id] == "awaiting_username_leetcode":
            try:
                username = message.text
                get_user_statistic = get_info_about_user(username)
                ranking = get_user_statistic.get('ranking', {})
                total_solved = get_user_statistic.get('totalSolved', {})
                contribution_points = get_user_statistic.get('contributionPoints', {})
                total_questions = get_user_statistic.get('totalQuestions', {})

                bot.send_message(user_id, f"Получена статистика для пользователя: \n Юзернейм: {username}\n Ранг: {ranking}\n Всего решено задач: {total_solved}\n Баллы вклада: {contribution_points}\n Всего вопросов: {total_questions}")

            except UserNotFoundError as e:
                bot.send_message(user_id, str(e))

            except Exception as e:
                bot.send_message(user_id, f"Произошла ошибка: {str(e)}")

            del states_users[user_id]
            return

    if message.text == "Codewars":
        bot.send_message(user_id, "Введите имя пользователя для получения статистики:")
        states_users[user_id] = "awaiting_username_codewars"
        return

    if message.text == "LeetCode":
        bot.send_message(user_id, "Введите имя пользователя для получения статистики:")
        states_users[user_id] = "awaiting_username_leetcode"
        return

# @bot.message_handler(commands=["/help"])
# def help_user(message):
#     bot.send_message(message.chat.id, "/start -  приветствие,\n /help - помощь, \n /codewars - получить статистику пользователя codewars")


bot.infinity_polling()


