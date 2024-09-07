import telebot
from telebot import types
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from datetime import datetime, timedelta
from db_class import Database

db = Database("Database1.db")
new_user_dict = {}
waiting_for_employee_message = {}


def get_current_working_week():
    # Дата начала отсчета рабочих недель
    # start_date = datetime(datetime.now().year, 1, 1)
    start_date = datetime(2024, 1, 1)
    today = datetime.now()
    # Рассчитайте количество недель с начала периода
    delta = today - start_date
    current_week = delta.days // 7 + 1
    return current_week


def ferst_message_maker(bot, message):
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


def handle_admin_messages(bot, message):
    if message.text == '/start':
        # Обработка сообщений администратора
        ferst_message_maker(bot, message)

    else:
        # print(message)
        id_user = message.from_user.id
        # Проверяем, что администратор в режиме ожидания пересланного сообщения
        if waiting_for_employee_message.get(id_user):
            tg_id_list = [tg_id[0] for tg_id in db.own_query(f'SELECT telegram_id FROM Users WHERE role = "employee"')]
            print(tg_id_list)
            if message.forward_from:
                print(message.forward_from)
                if message.forward_from.id not in tg_id_list:
                    # Сохраняем ID нового работника
                    new_user_dict['telegram_id'] = message.forward_from.id
                    new_user_dict['admin_id'] = id_user
                    bot.send_message(id_user, text='Введите данные нового работника в формате:\n'
                                                   'Имя: \n'
                                                   'Фамилия: \n'
                                                   'Отчество: \n'
                                                   'Номер телефона:\n'
                                                   'email:\n')
                    # Сбрасываем ожидание пересланного сообщения
                    waiting_for_employee_message[id_user] = False
                else:
                    bot.send_message(id_user, "Данный аккаунт уже зарегистрирован в качестве работника.")
            else:
                bot.send_message(id_user, "Невозможно получить id телеграм аккаунта пользователя.")

        elif 'telegram_id' in new_user_dict:
            # Ввод данных нового работника
            try:
                data = message.text.split('\n')
                new_user_dict['first_name'] = data[0].split(': ')[1]
                new_user_dict['second_name'] = data[1].split(': ')[1]
                new_user_dict['third_name'] = data[2].split(': ')[1]
                new_user_dict['phone_number'] = data[3].split(': ')[1]
                new_user_dict['email'] = data[4].split(': ')[1]

                # Внесение данных в базу
                db.own_query(
                    """INSERT INTO Users (telegram_id, first_name, second_name, third_name, phone_number, email, role, registration_date) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)""",
                    data=(
                        new_user_dict['telegram_id'],
                        new_user_dict['first_name'],
                        new_user_dict['second_name'],
                        new_user_dict['third_name'],
                        new_user_dict['phone_number'],
                        new_user_dict['email'],
                        'employee',
                        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    ),
                    fetch=False
                )
                db_user_id = db.own_query(f'SELECT id FROM Users '
                                          f'WHERE telegram_id = {new_user_dict['telegram_id']}'
                                          )[0][0]
                db.own_query(
                    """INSERT INTO Employees (user_id, hours_per_day, hours_per_week, week) 
                    VALUES (?, ?, ?, ?)""",
                    data=(
                        db_user_id,
                        0,
                        0,
                        get_current_working_week()
                    ),
                    fetch=False
                )

                bot.send_message(id_user, "Работник успешно добавлен в базу данных!")
                # Очистка данных после успешного добавления
                new_user_dict.clear()

                ferst_message_maker(bot, message)
            except Exception as e:
                bot.send_message(id_user, "Ошибка в формате данных. Попробуйте снова.")
                print(f"Error: {e}")
        else:
            # Обработка других текстовых сообщений (если необходимо)
            bot.send_message(id_user, "Данные не были запрошены. Неопознанный ввод.")
            pass


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
            zero_messsage_markup.add(types.InlineKeyboardButton("Расписание работников",
                                                                url='https://docs.google.com/spreadsheets/d/141XMzYf8'
                                                                    'kJkWdwuNqsdjuCQirxXaFEqGuCMRlWCJAlo/edit?gid=0#gid'
                                                                    '=0')
                                     )
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
            for i in workers_list[1]:
                print(i)
            print(len(workers_list[1]))
            workers_list_of_dicts = []

            for i in range(len(workers_list[1])):
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
                # Установить флаг ожидания пересланного сообщения
                waiting_for_employee_message[id_user] = True
                bot.send_message(id_user, text='Для начала процедуры добавления нового работника '
                                               'в базу данных требуется переслать сюда сообщение будущего работника.'
                                               '\n\n<em>В настройках приватности нового работника должна быть разрешена'
                                               ' пересылка сообщений</em>', parse_mode='HTML')
            elif data == 'add':
                # Вызов функции handle_text_messages для обработки текстовых сообщений
                handle_admin_messages(bot, call.message)

        if data == '2':
            if data == '0':
                pass

        if data == '3':
            text = ('Добро пожаловать, Господин Администратор!'
                    '\nПозвольте узнать, с чего Вам будет угодно начать сегодня, о великий Владыка!')
            zero_messsage_markup = types.InlineKeyboardMarkup()
            zero_messsage_markup.add(types.InlineKeyboardButton("Работники", callback_data="00"))
            zero_messsage_markup.add(types.InlineKeyboardButton("Заказы", callback_data="01"))
            zero_messsage_markup.add(types.InlineKeyboardButton("Отзывы", callback_data="02"))
            zero_messsage_markup.add(types.InlineKeyboardButton("Учёт и аудит", callback_data="03"))
            bot.edit_message_text(chat_id=id_user,
                                  message_id=call.message.message_id,
                                  text=text,
                                  reply_markup=zero_messsage_markup,
                                  parse_mode='HTML')


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
