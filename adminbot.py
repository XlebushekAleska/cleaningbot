import telebot
from telebot import types
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from datetime import datetime, timedelta
from db_class import Database

db = Database("Database1.db")

new_user_dict = {}


def handle_admin_messages(bot, message):
    # Обработка сообщений администратора
    text = ('Добро пожаловать, Господин Администратор!'
            '\nПозвольте узнать, с чего Вам будет угодно начать сегодня, о великий Владыка!')
    zero_messsage_markup = types.InlineKeyboardMarkup()
    zero_messsage_markup.add(types.InlineKeyboardButton("Работники", callback_data="00"))
    zero_messsage_markup.add(types.InlineKeyboardButton("Заказы", callback_data="01"))
    zero_messsage_markup.add(types.InlineKeyboardButton("Отзывы", callback_data="02"))
    zero_messsage_markup.add(types.InlineKeyboardButton("Учёт и аудит", callback_data="03"))
    bot.send_message(chat_id=message.chat.id,
                     text=text,
                     reply_markup=zero_messsage_markup)


def handle_admin_callback(bot, call):
    bot.answer_callback_query(callback_query_id=call.id, )
    id_user = call.message.chat.id
    flag = call.data[0:1]
    data = call.data[1:]

    if flag == '0':
        if data == '0':
            text = '<b>Работники</b>'
            zero_messsage_markup = types.InlineKeyboardMarkup()
            zero_messsage_markup.add(types.InlineKeyboardButton("Список работников", callback_data="10"))
            zero_messsage_markup.add(types.InlineKeyboardButton("Добавить работника", callback_data="11"))
            zero_messsage_markup.add(types.InlineKeyboardButton("Расписание работников", callback_data="12"))
            zero_messsage_markup.add(types.InlineKeyboardButton("Назад", callback_data="13"))
            bot.edit_message_text(chat_id=id_user,
                                  message_id=call.message.message_id,
                                  text=text,
                                  reply_markup=zero_messsage_markup,
                                  parse_mode='HTML')
    if flag == '1':
        if data[0] == '0':
            def review_index_generator(start, direction):
                index = start
                while True:
                    if direction == '+':
                        index += 1
                    elif direction == '-':
                        index -= 1
                    yield index

            def get_review_markup(index):
                review_markup = types.InlineKeyboardMarkup()
                review_markup.add(types.InlineKeyboardButton("Изменить расписание работника", callback_data=f"20"))
                # review_markup.add(types.InlineKeyboardButton("Удалить работника из базы данных", callback_data=f"2f"))
                review_markup.add(
                    types.InlineKeyboardButton("◀", callback_data=f"10{index}-"),
                    types.InlineKeyboardButton("▶", callback_data=f"10{index}+")
                )
                review_markup.add(types.InlineKeyboardButton("Назад", callback_data=f"00"))
                return review_markup

            workers_list = db.own_query("""SELECT * FROM Employees
                                                    INNER JOIN Users
                                                    ON Employees.user_id = Users.id
                                                    

                                                    """, columns=True)
            # INNER
            # JOIN
            # EmployeesSchedule
            # ON
            # Employees.id = EmployeesSchedule.employee_id

            workers_list_of_dicts = []

            for i in range(len(workers_list)):
                workers_list_of_dicts.append(zip(workers_list[0], workers_list[1][i]))

            if len(data) == 1:
                text = '<b>Работник:</b>\n\n'
                for key, value in workers_list_of_dicts[0]:
                    if key == 'id':
                        pass
                    else:
                        text += f'{key}: {value}\n'
                    # print(key, value)
                bot.edit_message_text(chat_id=id_user, message_id=call.message.message_id,
                                      text=text,
                                      reply_markup=get_review_markup(0),
                                      parse_mode='HTML')
            else:
                direction = data[-1]
                current_index = int(data[1:-1])
                gen = review_index_generator(current_index,
                                             direction)  # Используем генератор для получения нового индекса
                new_index = next(gen)

                if new_index < 0:
                    new_index = len(workers_list_of_dicts) - 1
                elif new_index >= len(workers_list_of_dicts):
                    new_index = 0

                # Изменяем сообщение только если новый индекс отличается от текущего
                if new_index != current_index:
                    text = '<b>Работник:</b>\n\n'
                    for key, value in workers_list_of_dicts[new_index]:
                        if key == 'id':
                            pass
                        else:
                            text += f'{key}: {value}\n'
                        # print(key, value)
                    bot.edit_message_text(chat_id=id_user,
                                          message_id=call.message.message_id,
                                          text=text,
                                          reply_markup=get_review_markup(new_index),
                                          parse_mode='HTML')

        if data[0] == '1':
            if data == '1':
                bot.send_message(id_user, text='Для начала процедуры добавления нового работника '
                                               'в базу данных требуется переслать сюда сообщение будущего работника')
            elif data == '1add':
                new_user_dict['telegram_id'] = id_user
                bot.send_message(new_user_dict['admin_id'], text='Введите данные нового работника в формате:\n'
                                                                 'Имя: \n'
                                                                 'Фамилия: \n'
                                                                 'Отчество: \n'
                                                                 'Номер телефона:\n'
                                                                 'email:\n'
                                 )


# основа под реализацию  добавления telegran_id нового работника в бд и заполнение его прочей информации

                # from telebot import TeleBot, types
                #
                # bot = TeleBot("YOUR_BOT_API_TOKEN")
                #
                # # Словарь для хранения состояний пользователей
                # waiting_for_forward = {}
                #
                # @bot.message_handler(commands=['start'])
                # def start_message(message):
                #     markup = types.InlineKeyboardMarkup()
                #     wait_for_forward_button = types.InlineKeyboardButton(text="Добавить сотрудника",
                #                                                          callback_data="wait_for_forward")
                #     markup.add(wait_for_forward_button)
                #     bot.send_message(message.chat.id, "Нажмите кнопку ниже, чтобы добавить нового сотрудника.",
                #                      reply_markup=markup)
                #
                # # Обработка нажатия кнопки
                # @bot.callback_query_handler(func=lambda call: call.data == "wait_for_forward")
                # def handle_wait_for_forward(call):
                #     admin_id = call.from_user.id
                #     waiting_for_forward[admin_id] = True  # Устанавливаем флаг ожидания пересланного сообщения
                #     bot.send_message(call.message.chat.id, "Отправьте пересланное сообщение от нового сотрудника.")
                #
                # # Обработка всех текстовых сообщений
                # @bot.message_handler(content_types=['text'])
                # def handle_message(message):
                #     admin_id = message.from_user.id
                #
                #     if waiting_for_forward.get(admin_id):
                #         if message.forward_from:
                #             employee_id = message.forward_from.id
                #             # Здесь добавьте код для внесения ID в базу данных
                #             bot.send_message(message.chat.id, f"ID сотрудника {employee_id} добавлен в базу данных.")
                #             waiting_for_forward[admin_id] = False  # Сбрасываем флаг ожидания пересланного сообщения
                #         else:
                #             bot.send_message(message.chat.id, "Пожалуйста, пересланное сообщение от сотрудника.")
                #     else:
                #         bot.send_message(message.chat.id, "Для добавления сотрудника нажмите соответствующую кнопку.")
                #
                # # Запуск бота
                # bot.polling()




# _________________________________________________________________________________________________________________________
# _________________________________________________________________________________________________________________________


# основа для генератора под клавиатуру с переключениями страниц

# def review_index_generator(start, direction):
#     index = start
#     while True:
#         if direction == '+':
#             index += 1
#         elif direction == '-':
#             index -= 1
#         yield index
#
#
# def get_review_markup(index):
#     review_markup = types.InlineKeyboardMarkup()
#     review_markup.add(
#         types.InlineKeyboardButton("◀", callback_data=f"03{index}-"),
#         types.InlineKeyboardButton("▶", callback_data=f"03{index}+")
#     )
#     review_markup.add(types.InlineKeyboardButton("Назад", callback_data=f"02"))
#     return review_markup
#
#
# feedback = db.own_query('SELECT * FROM Feedback WHERE rating >= 3')
# feedback_list = [
#     f"{''.join('★' * review[3] + '☆' * (5 - review[3]))}\n\nОтзыв: \n{review[4]}" for review in feedback
# ]
#
# if len(data) == 1:
#     bot.edit_message_text(chat_id=id_user, message_id=call.message.message_id,
#                           text=feedback_list[0],
#                           reply_markup=get_review_markup(0))
# else:
#     direction = data[-1]
#     current_index = int(data[1:-1])
#     gen = review_index_generator(current_index,
#                                  direction)  # Используем генератор для получения нового индекса
#     new_index = next(gen)
#
#     if new_index < 0:
#         new_index = len(feedback_list) - 1
#     elif new_index >= len(feedback_list):
#         new_index = 0
#
#     # Изменяем сообщение только если новый индекс отличается от текущего
#     if new_index != current_index:
#         bot.edit_message_text(chat_id=id_user, message_id=call.message.message_id,
#                               text=feedback_list[new_index],
#                               reply_markup=get_review_markup(new_index))
