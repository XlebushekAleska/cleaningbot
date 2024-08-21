import telebot
from telebot import types
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from datetime import datetime, timedelta


def handle_worker_messages(bot, message):
    # Обработка сообщений работников
    bot.send_message(message.chat.id, "Вы вошли как работник.")


def handle_worker_callback(bot, call):
    if call.data == "worker_button":
        bot.answer_callback_query(call.id, "Вы нажали рабочую кнопку.")
        bot.send_message(call.message.chat.id, "Рабочая команда выполнена.")
