from db_class import Database

db = Database("Database1.db")

tg_id_list = db.own_query(f'SELECT telegram_id FROM Users WHERE role = "employee"')

print(tg_id_list)

# from datetime import datetime, timedelta
#
#
# def get_current_working_week():
#     # Дата начала отсчета рабочих недель
#     start_date = datetime(datetime.now().year, 1, 1)
#     today = datetime.now()
#     # Рассчитайте количество недель с начала периода
#     delta = today - start_date
#     current_week = delta.days // 7 + 1
#     return current_week
#
#
# print(get_current_working_week())


#
# t = [(1, 1, 1, 4, 'полная хуйня, но мне понравилось', '2024-08-19 15:33:07'), (2, 1, 2, 5, 'вот это заебись, богоугодная хуйня', '2024-08-19 15:33:59')]
# r = []
# for review in t:
#     r.append(f"{('★' * review[3] + '☆' * (5 - review[3]))}\n\nОтзыв: \n{review[4]}")
#
# for i in r:
#     print(i)


# import gspread
# from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
#
# import telebot
# from telebot import types
# from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
# from datetime import datetime, timedelta
# import adminbot
# import workerbot
#
# bot = telebot.TeleBot('6510684394:AAFsvSNzEk8GYqfRjRnO6N6WSsMMWWhi3Ic')
# workers_list = [769963229]
# admins_list = [769963229]
# user_data = {}
#
# # Обработчик текстовых сообщений
# @bot.message_handler(func=lambda message: True)
# def echo_message(message):
#     if message.text == "/start":
#         if message.chat.id in admins_list:
#             adminbot.start(message)
#
#         elif message.chat.id in workers_list:
#             workerbot.start(message)
#
#         else:
#             pass
#
#
#
#
# @bot.callback_query_handler(func=lambda call: True)
# def query_handler(call):
#     bot.answer_callback_query(callback_query_id=call.id, )
#     id_user = call.message.chat.id
#     flag = call.data[0:1]
#     data = call.data[1:]
#
#     if flag == '1':
#         if data == "r-" and user_data[id_user]['rooms'] > 1:
#             user_data[id_user]['rooms'] -= 1
#         elif data == "r+" and user_data[id_user]['rooms'] < 10:
#             pass
#
#
#
#
# print("Ready")
# bot.infinity_polling()

# _______________________________________________________________________________________________________________________
# _______________________________________________________________________________________________________________________
# _______________________________________________________________________________________________________________________
# _______________________________________________________________________________________________________________________
# __________________________________________ниже рабочий код с четверга__________________________________________________
# __________________________________________________15.08.2024___________________________________________________________
# _______________________________________________________________________________________________________________________

#
# # import gspread
# # from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
#
# import telebot
# from telebot import types
# from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
#
# bot = telebot.TeleBot('6510684394:AAFsvSNzEk8GYqfRjRnO6N6WSsMMWWhi3Ic')
# workers_list = [769963229]
# admins_list = []
# user_data = {}
#
#
# def first_message_maker(user_id):
#     global user_data
#     message = ""
#     for key, value in user_data[user_id].items():
#         if key == 'rooms':
#             if value == 1:
#                 message += "1 комната"
#             elif 2 <= value < 5:
#                 message += f"{str(value)} комнаты"
#             else:
#                 message += f"{str(value)} комнат"
#             message += ", "
#             rooms_price = value * 14
#             rooms_time = value
#         if key == 'bathrooms':
#             if value == 1:
#                 message += "1 санузел"
#             elif 2 <= value < 5:
#                 message += f"{str(value)} санузла"
#             else:
#                 message += f"{str(value)} санузлов"
#             message += "."
#             bathrooms_price = value * 20
#             bathrooms_time = value * 0.5
#
#     user_data[user_id]['price'] = 31 + rooms_price + bathrooms_price
#     user_data[user_id]['cleaning_time'] = 2 + rooms_time + bathrooms_time
#     return message
#
#
# def first_message_text(call):
#     id_user = call.message.chat.id
#     text = f"""
# Добро пожаловать в бота-ассистента
# клининговой компании <b>"КлинниБогинни"!</b>
#
# Я помогу Вам ознакомиться со списком услуг,
# рассчитать стоимость заказа, а также
# посмотреть и оставить отзывы о нашей компании!
#
# <a href="https://drive.google.com/file/d/1gH8ogErgeWSeqIPhM9XQVPitbmzHxG1v/view">Из чего состоит базовая уборка: чек-лист</a>
#
# Для изменения основных параметров заказа
# воспользуйтесь клавиатурой ниже. Ваш заказ
# включает в себя сейчас:
#
# {first_message_maker(id_user)}
# <b>{user_data[id_user]['price']}BYN.</b>
#
# <em>1 санузел = 1 ванная + 1 туалет
# (неважно, совмещенные или раздельные)
# Кухня и коридор включены в стоимость.</em>
# """
#     markup = types.InlineKeyboardMarkup()
#     markup.add(
#         types.InlineKeyboardButton("-", callback_data="1r-"),
#         types.InlineKeyboardButton("комната", callback_data="1np"),
#         types.InlineKeyboardButton("+", callback_data="1r+"))
#     markup.add(
#         types.InlineKeyboardButton("-", callback_data="1b-"),
#         types.InlineKeyboardButton("санузел", callback_data="1np"),
#         types.InlineKeyboardButton("+", callback_data="1b+"))
#     markup.add(types.InlineKeyboardButton("Рассчитать уборку", callback_data="1or"))
#
#     # Редактирование текста сообщения и обновление клавиатуры
#     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                           text=text, parse_mode='HTML', reply_markup=markup)
#
#
# def second_message_text(call):
#     id_user = call.message.chat.id
#     text = f"Дополнительные опции:\n"
#
#     if user_data[id_user]['linen']:
#         text += f'\nПогладим белье - {user_data[id_user]['linen']} ч'
#     if user_data[id_user]['windows']:
#         text += f'\nПомоем окна - {user_data[id_user]['windows']} шт'
#     if user_data[id_user]['balcony']:
#         text += f'\nУберём на балконе - {user_data[id_user]['balcony']} шт'
#
#     additional_markup = types.InlineKeyboardMarkup()
#     additional_markup.add(
#         types.InlineKeyboardButton("-", callback_data="6c-"),
#         types.InlineKeyboardButton("Погладим\nбельё (ч)", callback_data="6np"),
#         types.InlineKeyboardButton("+", callback_data="6c+"))
#
#     additional_markup.add(
#         types.InlineKeyboardButton("-", callback_data="6w-"),
#         types.InlineKeyboardButton("Помоем\nокна (шт)", callback_data="6np"),
#         types.InlineKeyboardButton("+", callback_data="6w+"))
#
#     additional_markup.add(
#         types.InlineKeyboardButton("-", callback_data="6b-"),
#         types.InlineKeyboardButton("Уберём на\nбалконе (шт)", callback_data="6np"),
#         types.InlineKeyboardButton("+", callback_data="6b+"))
#
#     additional_markup.add(types.InlineKeyboardButton("Далее", callback_data="6or"))
#
#     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                           text=text, parse_mode='HTML', reply_markup=additional_markup)
#
#
# @bot.callback_query_handler(func=DetailedTelegramCalendar.func())
# def cal(c):
#     result, key, step = DetailedTelegramCalendar().process(c.data)
#     if not result and key:
#         # Select {LSTEP[step]}
#         bot.edit_message_text(f"Выберите дату:",
#                               c.message.chat.id,
#                               c.message.message_id,
#                               reply_markup=key)
#     elif result:
#         bot.edit_message_text(f"Дата уборки: {result}",
#                               c.message.chat.id,
#                               c.message.message_id)
#         global user_data
#         user_data[c.from_user.id]['date'] = result
#         time_markup = types.InlineKeyboardMarkup()
#         for i in range(9, 19):
#             time_markup.add(types.InlineKeyboardButton(f"{str(i) + ':00'}", callback_data=f"2{str(i) + ':00'}"))
#             time_markup.add(types.InlineKeyboardButton(f"{str(i) + ':30'}", callback_data=f"2{str(i) + ':30'}"))
#         bot.send_message(c.message.chat.id, "Выберите время:", parse_mode='HTML', reply_markup=time_markup)
#
#
# # Обработчик текстовых сообщений
# @bot.message_handler(func=lambda message: True)
# def echo_message(message):
#     if message.text == "/start":
#         if message.chat.id not in user_data:
#             user_data[message.chat.id] = {
#                 'rooms': 1,
#                 'bathrooms': 1,
#                 'price': 31,
#                 'discount': 0,
#                 'cleaning_time': 2,
#                 'date': '',
#                 'time': '',
#                 'frequency': '',
#                 'refrigerator': False,
#                 'oven': False,
#                 'boxes': False,
#                 'dishes': False,
#                 'microwave': False,
#                 'linen': 0,
#                 'windows': 0,
#                 'balcony': 0,
#                 'street': '',
#                 'house': '',
#                 'body': '',
#                 'apartment': '',
#                 'first_name': '',
#                 'second_name': '',
#                 'third_name': '',
#                 'phone_number': '',
#                 'email': '',
#             }
#
#         markup = types.InlineKeyboardMarkup()
#         markup.add(
#             types.InlineKeyboardButton("-", callback_data="1r-"),
#             types.InlineKeyboardButton("комната", callback_data="1np"),
#             types.InlineKeyboardButton("+", callback_data="1r+"))
#
#         markup.add(
#             types.InlineKeyboardButton("-", callback_data="1b-"),
#             types.InlineKeyboardButton("санузел", callback_data="1np"),
#             types.InlineKeyboardButton("+", callback_data="1b+"))
#
#         markup.add(types.InlineKeyboardButton("Рассчитать уборку", callback_data="1or"))
#
#         bot.send_message(message.chat.id, f"""
# Добро пожаловать в бота-ассистента
# клининговой компании <b>"КлинниБогинни"!</b>
#
# Я помогу Вам ознакомиться со списком услуг,
# рассчитать стоимость заказа, а также
# посмотреть и оставить отзывы о нашей компании!
#
# <a href="https://drive.google.com/file/d/1gH8ogErgeWSeqIPhM9XQVPitbmzHxG1v/view">Из чего состоит базовая уборка: чек-лист</a>
#
# Для изменения основных параметров заказа
# воспользуйтесь клавиатурой ниже. Ваш заказ
# включает в себя сейчас:
#
# {first_message_maker(message.chat.id)}
# <b>{user_data[message.chat.id]['price']}BYN.</b>
#
# <em>1 санузел = 1 ванная + 1 туалет
# (неважно, совмещенные или раздельные)
# Кухня и коридор включены в стоимость.</em>
# """, parse_mode='HTML', reply_markup=markup)
#
#         print(message)
#         # bot.send_message(message.chat.id, text=message)
#
#
# @bot.callback_query_handler(func=lambda call: True)
# def query_handler(call):
#     bot.answer_callback_query(callback_query_id=call.id, )
#     id_user = call.message.chat.id
#     flag = call.data[0:1]
#     data = call.data[1:]
#
#     if flag == '1':
#         if data == "r-" and user_data[id_user]['rooms'] > 1:
#             user_data[id_user]['rooms'] -= 1
#             first_message_text(call)
#         elif data == "r+" and user_data[id_user]['rooms'] < 10:
#             user_data[id_user]['rooms'] += 1
#             first_message_text(call)
#         elif data == "b-" and user_data[id_user]['bathrooms'] > 1:
#             user_data[id_user]['bathrooms'] -= 1
#             first_message_text(call)
#         elif data == "b+" and user_data[id_user]['bathrooms'] < 10:
#             user_data[id_user]['bathrooms'] += 1
#             first_message_text(call)
#         elif data == "np":
#             pass
#         elif data == "or":
#             calendar, step = DetailedTelegramCalendar().build()
#             bot.send_message(id_user,
#                              f"Select {LSTEP[step]}",
#                              reply_markup=calendar)
#             print(user_data)
#
#     elif flag == '2':
#         user_data[id_user]['time'] = data
#         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                               text=f'Время: {data}', parse_mode='HTML')
#
#         frequency_markup = types.InlineKeyboardMarkup()
#         frequency_markup.add(types.InlineKeyboardButton("Раз в неделю\n15%", callback_data="315"))
#         frequency_markup.add(types.InlineKeyboardButton("Раз в две недели\n10%", callback_data="310"))
#         frequency_markup.add(types.InlineKeyboardButton("Раз в месяц\n7%", callback_data="37"))
#         frequency_markup.add(types.InlineKeyboardButton("1 или первый раз", callback_data="30"))
#         bot.send_message(id_user, "Как часто у вас убираться:", parse_mode='HTML', reply_markup=frequency_markup)
#
#     elif flag == '3':
#         if data == "15":
#             user_data[id_user]['frequency'] = "раз в неделю"
#             user_data[id_user]['discount'] = 0.15
#             bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                   text='раз в неделю - 15%', parse_mode='HTML')
#         elif data == "10":
#             user_data[id_user]['frequency'] = "раз в две недели"
#             user_data[id_user]['discount'] = 0.1
#             bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                   text='раз в две недели - 10%', parse_mode='HTML')
#         elif data == "7":
#             user_data[id_user]['frequency'] = "раз в месяц"
#             user_data[id_user]['discount'] = 0.07
#             bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                   text='раз в месяц - 7%', parse_mode='HTML')
#         elif data == "0":
#             user_data[id_user]['frequency'] = "1 раз или первый раз"
#             user_data[id_user]['discount'] = 0
#             bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                   text='1 раз или первый раз', parse_mode='HTML')
#
#         additional_markup = types.InlineKeyboardMarkup()
#         additional_markup.add(types.InlineKeyboardButton("Внутри холодильника", callback_data="41"))
#         additional_markup.add(types.InlineKeyboardButton("Внутри духовки", callback_data="42"))
#         additional_markup.add(types.InlineKeyboardButton("Внутри кухонных шкафов", callback_data="43"))
#         additional_markup.add(types.InlineKeyboardButton("Помоем посуду", callback_data="44"))
#         additional_markup.add(types.InlineKeyboardButton("Внутри микроволновки", callback_data="45"))
#         additional_markup.add(types.InlineKeyboardButton("Далее", callback_data="50"))
#         bot.send_message(id_user, "Дополнительные опции:", parse_mode='HTML', reply_markup=additional_markup)
#
#     elif flag == '4':
#         additional_markup = types.InlineKeyboardMarkup()
#         if data == "1":
#             if not user_data[id_user]['refrigerator']:
#                 user_data[id_user]['refrigerator'] = True
#                 user_data[id_user]['price'] += 25
#                 user_data[id_user]['cleaning_time'] += 1
#             else:
#                 user_data[id_user]['refrigerator'] = False
#                 user_data[id_user]['price'] -= 25
#                 user_data[id_user]['cleaning_time'] -= 1
#         elif data == "2":
#             if not user_data[id_user]['oven']:
#                 user_data[id_user]['oven'] = True
#                 user_data[id_user]['price'] += 25
#                 user_data[id_user]['cleaning_time'] += 1
#             else:
#                 user_data[id_user]['oven'] = False
#                 user_data[id_user]['price'] -= 25
#                 user_data[id_user]['cleaning_time'] -= 1
#         elif data == "3":
#             if not user_data[id_user]['boxes']:
#                 user_data[id_user]['boxes'] = True
#                 user_data[id_user]['price'] += 25
#                 user_data[id_user]['cleaning_time'] += 1
#             else:
#                 user_data[id_user]['boxes'] = False
#                 user_data[id_user]['price'] -= 25
#                 user_data[id_user]['cleaning_time'] -= 1
#         elif data == "4":
#             if not user_data[id_user]['dishes']:
#                 user_data[id_user]['dishes'] = True
#                 user_data[id_user]['price'] += 10
#                 user_data[id_user]['cleaning_time'] += 0.5
#             else:
#                 user_data[id_user]['dishes'] = False
#                 user_data[id_user]['price'] -= 10
#                 user_data[id_user]['cleaning_time'] -= 0.5
#         elif data == "5":
#             if not user_data[id_user]['microwave']:
#                 user_data[id_user]['microwave'] = True
#                 user_data[id_user]['price'] += 20
#                 user_data[id_user]['cleaning_time'] += 0.5
#             else:
#                 user_data[id_user]['microwave'] = False
#                 user_data[id_user]['price'] -= 20
#                 user_data[id_user]['cleaning_time'] -= 0.5
#
#         if user_data[id_user]['refrigerator']:
#             additional_markup.add(types.InlineKeyboardButton("Внутри холодильника✅", callback_data="41"))
#         else:
#             additional_markup.add(types.InlineKeyboardButton("Внутри холодильника", callback_data="41"))
#
#         if user_data[id_user]['oven']:
#             additional_markup.add(types.InlineKeyboardButton("Внутри духовки✅", callback_data="42"))
#         else:
#             additional_markup.add(types.InlineKeyboardButton("Внутри духовки", callback_data="42"))
#
#         if user_data[id_user]['boxes']:
#             additional_markup.add(types.InlineKeyboardButton("Внутри кухонных шкафов✅", callback_data="43"))
#         else:
#             additional_markup.add(types.InlineKeyboardButton("Внутри кухонных шкафов", callback_data="43"))
#
#         if user_data[id_user]['dishes']:
#             additional_markup.add(types.InlineKeyboardButton("Помоем посуду✅", callback_data="44"))
#         else:
#             additional_markup.add(types.InlineKeyboardButton("Помоем посуду", callback_data="44"))
#
#         if user_data[id_user]['microwave']:
#             additional_markup.add(types.InlineKeyboardButton("Внутри микроволновки✅", callback_data="45"))
#         else:
#             additional_markup.add(types.InlineKeyboardButton("Внутри микроволновки", callback_data="45"))
#         additional_markup.add(types.InlineKeyboardButton("Далее", callback_data="50"))
#         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                               text='Дополнительные опции:', parse_mode='HTML', reply_markup=additional_markup)
#
#     elif flag == '5':
#         if data == '0':
#             bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                   text=f"""
# Дополнительные опции:
# {'\nВнутри холодильника' if user_data[id_user]['refrigerator'] else ''}{'\nВнутри духовки' if user_data[id_user]['oven'] else ''}{'\nВнутри кухонных шкафов' if user_data[id_user]['boxes'] else ''}{'\nПомоем посуду' if user_data[id_user]['dishes'] else ''}{'\nВнутри микроволновки' if user_data[id_user]['microwave'] else ''}
# """, parse_mode='HTML')
#             additional_markup = types.InlineKeyboardMarkup()
#             additional_markup.add(
#                 types.InlineKeyboardButton("-", callback_data="6c-"),
#                 types.InlineKeyboardButton("Погладим\nбельё (ч)", callback_data="6np"),
#                 types.InlineKeyboardButton("+", callback_data="6c+"))
#
#             additional_markup.add(
#                 types.InlineKeyboardButton("-", callback_data="6w-"),
#                 types.InlineKeyboardButton("Помоем\nокна (шт)", callback_data="6np"),
#                 types.InlineKeyboardButton("+", callback_data="6w+"))
#
#             additional_markup.add(
#                 types.InlineKeyboardButton("-", callback_data="6b-"),
#                 types.InlineKeyboardButton("Уберём на\nбалконе (шт)", callback_data="6np"),
#                 types.InlineKeyboardButton("+", callback_data="6b+"))
#
#             additional_markup.add(types.InlineKeyboardButton("Далее", callback_data="6or"))
#             bot.send_message(id_user, "Дополнительные опции:", parse_mode='HTML', reply_markup=additional_markup)
#
#     elif flag == '6':
#         if data == "c-" and user_data[id_user]['linen'] > 0:
#             user_data[id_user]['linen'] -= 1
#             user_data[id_user]['price'] -= 20
#             second_message_text(call)
#         elif data == "c+" and user_data[id_user]['linen'] < 11:
#             user_data[id_user]['linen'] += 1
#             user_data[id_user]['price'] += 20
#             second_message_text(call)
#         elif data == "w-" and user_data[id_user]['windows'] > 0:
#             user_data[id_user]['windows'] -= 1
#             user_data[id_user]['price'] -= 15
#             second_message_text(call)
#         elif data == "w+" and user_data[id_user]['windows'] < 15:
#             user_data[id_user]['windows'] += 1
#             user_data[id_user]['price'] += 15
#             second_message_text(call)
#         elif data == "b-" and user_data[id_user]['balcony'] > 0:
#             user_data[id_user]['balcony'] -= 1
#             user_data[id_user]['price'] -= 20
#             second_message_text(call)
#         elif data == "b+" and user_data[id_user]['balcony'] < 6:
#             user_data[id_user]['balcony'] += 1
#             user_data[id_user]['price'] += 20
#             second_message_text(call)
#         elif data == "np":
#             pass
#         elif data == "or":
#             text = 'Дополнительные опции:\n'
#             if user_data[id_user]['linen']:
#                 text += f'\nПогладим белье - {user_data[id_user]['linen']} ч'
#             if user_data[id_user]['windows']:
#                 text += f'\nПомоем окна - {user_data[id_user]['windows']} шт'
#             if user_data[id_user]['balcony']:
#                 text += f'\nУберём на балконе - {user_data[id_user]['balcony']} шт'
#             bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                   text=text)
#             bot.send_message(id_user, "Введите свой адрес в формате:\n<em>Улица, Дом, Корпус, Квартира</em>",
#                              parse_mode='HTML')
#
#
# print("Ready")
# bot.infinity_polling()


# _______________________________________________________________________________________________________________________
# _______________________________________________________________________________________________________________________
# _______________________________________________________________________________________________________________________
# _______________________________________________________________________________________________________________________
# _______________________________________________________________________________________________________________________
# _______________________________________________________________________________________________________________________
# _______________________________________________________________________________________________________________________


# # import gspread
# # from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
#
# import telebot
# from telebot import types
# from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
#
# bot = telebot.TeleBot('6510684394:AAFsvSNzEk8GYqfRjRnO6N6WSsMMWWhi3Ic')
# workers_list = [769963229]
# admins_list = []
# user_data = {}
#
#
# def first_message_maker(user_id):
#     global user_data
#     message = ""
#     for key, value in user_data[user_id].items():
#         if key == 'rooms':
#             if value == 1:
#                 message += "1 комната"
#             elif 2 <= value < 5:
#                 message += f"{str(value)} комнаты"
#             else:
#                 message += f"{str(value)} комнат"
#             message += ", "
#             rooms_price = value * 14
#             rooms_time = value
#         if key == 'bathrooms':
#             if value == 1:
#                 message += "1 санузел"
#             elif 2 <= value < 5:
#                 message += f"{str(value)} санузла"
#             else:
#                 message += f"{str(value)} санузлов"
#             message += "."
#             bathrooms_price = value * 20
#             bathrooms_time = value * 0.5
#
#     user_data[user_id]['price'] = 31 + rooms_price + bathrooms_price
#     user_data[user_id]['cleaning_time'] = 2 + rooms_time + bathrooms_time
#     return message
#
#
# def first_message_text(call):
#     id_user = call.message.chat.id
#     text = f"""
# Добро пожаловать в бота-ассистента
# клининговой компании <b>"КлинниБогинни"!</b>
#
# Я помогу Вам ознакомиться со списком услуг,
# рассчитать стоимость заказа, а также
# посмотреть и оставить отзывы о нашей компании!
#
# <a href="https://drive.google.com/file/d/1gH8ogErgeWSeqIPhM9XQVPitbmzHxG1v/view">Из чего состоит базовая уборка: чек-лист</a>
#
# Для изменения основных параметров заказа
# воспользуйтесь клавиатурой ниже. Ваш заказ
# включает в себя сейчас:
#
# {first_message_maker(id_user)}
# <b>{user_data[id_user]['price']}BYN.</b>
#
# <em>1 санузел = 1 ванная + 1 туалет
# (неважно, совмещенные или раздельные)
# Кухня и коридор включены в стоимость.</em>
# """
#     markup = types.InlineKeyboardMarkup()
#     markup.add(
#         types.InlineKeyboardButton("-", callback_data="1r-"),
#         types.InlineKeyboardButton("комната", callback_data="1np"),
#         types.InlineKeyboardButton("+", callback_data="1r+"))
#     markup.add(
#         types.InlineKeyboardButton("-", callback_data="1b-"),
#         types.InlineKeyboardButton("санузел", callback_data="1np"),
#         types.InlineKeyboardButton("+", callback_data="1b+"))
#     markup.add(types.InlineKeyboardButton("Рассчитать уборку", callback_data="1or"))
#
#     # Редактирование текста сообщения и обновление клавиатуры
#     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                           text=text, parse_mode='HTML', reply_markup=markup)
#
#
# def second_message_text(call):
#     id_user = call.message.chat.id
#     text = f"Дополнительные опции:\n"
#
#     if user_data[id_user]['linen']:
#         text += f'\nПогладим белье - {user_data[id_user]['linen']} ч'
#     if user_data[id_user]['windows']:
#         text += f'\nПомоем окна - {user_data[id_user]['windows']} шт'
#     if user_data[id_user]['balcony']:
#         text += f'\nУберём на балконе - {user_data[id_user]['balcony']} шт'
#
#     additional_markup = types.InlineKeyboardMarkup()
#     additional_markup.add(
#         types.InlineKeyboardButton("-", callback_data="6c-"),
#         types.InlineKeyboardButton("Погладим\nбельё (ч)", callback_data="6np"),
#         types.InlineKeyboardButton("+", callback_data="6c+"))
#
#     additional_markup.add(
#         types.InlineKeyboardButton("-", callback_data="6w-"),
#         types.InlineKeyboardButton("Помоем\nокна (шт)", callback_data="6np"),
#         types.InlineKeyboardButton("+", callback_data="6w+"))
#
#     additional_markup.add(
#         types.InlineKeyboardButton("-", callback_data="6b-"),
#         types.InlineKeyboardButton("Уберём на\nбалконе (шт)", callback_data="6np"),
#         types.InlineKeyboardButton("+", callback_data="6b+"))
#
#     additional_markup.add(types.InlineKeyboardButton("Далее", callback_data="6or"))
#
#     bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                           text=text, parse_mode='HTML', reply_markup=additional_markup)
#
#
# @bot.callback_query_handler(func=DetailedTelegramCalendar.func())
# def cal(c):
#     result, key, step = DetailedTelegramCalendar().process(c.data)
#     if not result and key:
#         # Select {LSTEP[step]}
#         bot.edit_message_text(f"Выберите дату:",
#                               c.message.chat.id,
#                               c.message.message_id,
#                               reply_markup=key)
#     elif result:
#         bot.edit_message_text(f"Дата уборки: {result}",
#                               c.message.chat.id,
#                               c.message.message_id)
#         global user_data
#         user_data[c.from_user.id]['date'] = result
#         time_markup = types.InlineKeyboardMarkup()
#         for i in range(9, 19):
#             time_markup.add(types.InlineKeyboardButton(f"{str(i) + ':00'}", callback_data=f"2{str(i) + ':00'}"))
#             time_markup.add(types.InlineKeyboardButton(f"{str(i) + ':30'}", callback_data=f"2{str(i) + ':30'}"))
#         bot.send_message(c.message.chat.id, "Выберите время:", parse_mode='HTML', reply_markup=time_markup)
#
#
# # Обработчик текстовых сообщений
# @bot.message_handler(func=lambda message: True)
# def echo_message(message):
#     if message.chat.id not in user_data:
#         user_data[message.chat.id] = {
#             'rooms': 1,
#             'bathrooms': 1,
#             'price': 31,
#             'discount': 0,
#             'cleaning_time': 2,
#             'date': '',
#             'time': '',
#             'frequency': '',
#             'refrigerator': False,
#             'oven': False,
#             'boxes': False,
#             'dishes': False,
#             'microwave': False,
#             'linen': 0,
#             'windows': 0,
#             'balcony': 0,
#             'street': '',
#             'house': '',
#             'body': '',
#             'apartment': '',
#             'first_name': '',
#             'flast_name': '',
#             'third_name': '',
#             'phone_number': '',
#             'email': '',
#         }
#     if message.text == "/start":
#         markup = types.InlineKeyboardMarkup()
#         markup.add(
#             types.InlineKeyboardButton("-", callback_data="1r-"),
#             types.InlineKeyboardButton("комната", callback_data="1np"),
#             types.InlineKeyboardButton("+", callback_data="1r+"))
#
#         markup.add(
#             types.InlineKeyboardButton("-", callback_data="1b-"),
#             types.InlineKeyboardButton("санузел", callback_data="1np"),
#             types.InlineKeyboardButton("+", callback_data="1b+"))
#
#         markup.add(types.InlineKeyboardButton("Рассчитать уборку", callback_data="1or"))
#
#         bot.send_message(message.chat.id, f"""
# Добро пожаловать в бота-ассистента
# клининговой компании <b>"КлинниБогинни"!</b>
#
# Я помогу Вам ознакомиться со списком услуг,
# рассчитать стоимость заказа, а также
# посмотреть и оставить отзывы о нашей компании!
#
# <a href="https://drive.google.com/file/d/1gH8ogErgeWSeqIPhM9XQVPitbmzHxG1v/view">Из чего состоит базовая уборка: чек-лист</a>
#
# Для изменения основных параметров заказа
# воспользуйтесь клавиатурой ниже. Ваш заказ
# включает в себя сейчас:
#
# {first_message_maker(message.chat.id)}
# <b>{user_data[message.chat.id]['price']}BYN.</b>
#
# <em>1 санузел = 1 ванная + 1 туалет
# (неважно, совмещенные или раздельные)
# Кухня и коридор включены в стоимость.</em>
# """, parse_mode='HTML', reply_markup=markup)
#
#     if 'Адрес' in message.text:
#         print(message)
#         bot.send_message(message.chat.id, text=message)
#         print(message.text[message.text.index(":")+1:].split(', '))
#         adress = message.text[message.text.index(":") + 1:].split(', ')
#         user_data[message.chat.id]['street'] = adress[0]
#         user_data[message.chat.id]['house'] = adress[1]
#         user_data[message.chat.id]['body'] = adress[2]
#         user_data[message.chat.id]['apartment'] = adress[3]
#         print(user_data)
#
#     if 'Контакты'in message.text:
#
#         pass
#
#
#
# @bot.callback_query_handler(func=lambda call: True)
# def query_handler(call):
#     bot.answer_callback_query(callback_query_id=call.id, )
#     id_user = call.message.chat.id
#     flag = call.data[0:1]
#     data = call.data[1:]
#
#     if flag == '1':
#         if data == "r-" and user_data[id_user]['rooms'] > 1:
#             user_data[id_user]['rooms'] -= 1
#             first_message_text(call)
#         elif data == "r+" and user_data[id_user]['rooms'] < 10:
#             user_data[id_user]['rooms'] += 1
#             first_message_text(call)
#         elif data == "b-" and user_data[id_user]['bathrooms'] > 1:
#             user_data[id_user]['bathrooms'] -= 1
#             first_message_text(call)
#         elif data == "b+" and user_data[id_user]['bathrooms'] < 10:
#             user_data[id_user]['bathrooms'] += 1
#             first_message_text(call)
#         elif data == "np":
#             pass
#         elif data == "or":
#             calendar, step = DetailedTelegramCalendar().build()
#             bot.send_message(id_user,
#                              f"Select {LSTEP[step]}",
#                              reply_markup=calendar)
#
#     elif flag == '2':
#         user_data[id_user]['time'] = data
#         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                               text=f'Время: {data}', parse_mode='HTML')
#
#         frequency_markup = types.InlineKeyboardMarkup()
#         frequency_markup.add(types.InlineKeyboardButton("Раз в неделю\n15%", callback_data="315"))
#         frequency_markup.add(types.InlineKeyboardButton("Раз в две недели\n10%", callback_data="310"))
#         frequency_markup.add(types.InlineKeyboardButton("Раз в месяц\n7%", callback_data="37"))
#         frequency_markup.add(types.InlineKeyboardButton("1 или первый раз", callback_data="30"))
#         bot.send_message(id_user, "Как часто у вас убираться:", parse_mode='HTML', reply_markup=frequency_markup)
#
#     elif flag == '3':
#         if data == "15":
#             user_data[id_user]['frequency'] = "раз в неделю"
#             user_data[id_user]['discount'] = 0.15
#             bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                   text='раз в неделю - 15%', parse_mode='HTML')
#         elif data == "10":
#             user_data[id_user]['frequency'] = "раз в две недели"
#             user_data[id_user]['discount'] = 0.1
#             bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                   text='раз в две недели - 10%', parse_mode='HTML')
#         elif data == "7":
#             user_data[id_user]['frequency'] = "раз в месяц"
#             user_data[id_user]['discount'] = 0.07
#             bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                   text='раз в месяц - 7%', parse_mode='HTML')
#         elif data == "0":
#             user_data[id_user]['frequency'] = "1 раз или первый раз"
#             user_data[id_user]['discount'] = 0
#             bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                   text='1 раз или первый раз', parse_mode='HTML')
#
#         additional_markup = types.InlineKeyboardMarkup()
#         additional_markup.add(types.InlineKeyboardButton("Внутри холодильника", callback_data="41"))
#         additional_markup.add(types.InlineKeyboardButton("Внутри духовки", callback_data="42"))
#         additional_markup.add(types.InlineKeyboardButton("Внутри кухонных шкафов", callback_data="43"))
#         additional_markup.add(types.InlineKeyboardButton("Помоем посуду", callback_data="44"))
#         additional_markup.add(types.InlineKeyboardButton("Внутри микроволновки", callback_data="45"))
#         additional_markup.add(types.InlineKeyboardButton("Далее", callback_data="50"))
#         bot.send_message(id_user, "Дополнительные опции:", parse_mode='HTML', reply_markup=additional_markup)
#
#     elif flag == '4':
#         additional_markup = types.InlineKeyboardMarkup()
#         if data == "1":
#             if not user_data[id_user]['refrigerator']:
#                 user_data[id_user]['refrigerator'] = True
#                 user_data[id_user]['price'] += 25
#                 user_data[id_user]['cleaning_time'] += 1
#             else:
#                 user_data[id_user]['refrigerator'] = False
#                 user_data[id_user]['price'] -= 25
#                 user_data[id_user]['cleaning_time'] -= 1
#         elif data == "2":
#             if not user_data[id_user]['oven']:
#                 user_data[id_user]['oven'] = True
#                 user_data[id_user]['price'] += 25
#                 user_data[id_user]['cleaning_time'] += 1
#             else:
#                 user_data[id_user]['oven'] = False
#                 user_data[id_user]['price'] -= 25
#                 user_data[id_user]['cleaning_time'] -= 1
#         elif data == "3":
#             if not user_data[id_user]['boxes']:
#                 user_data[id_user]['boxes'] = True
#                 user_data[id_user]['price'] += 25
#                 user_data[id_user]['cleaning_time'] += 1
#             else:
#                 user_data[id_user]['boxes'] = False
#                 user_data[id_user]['price'] -= 25
#                 user_data[id_user]['cleaning_time'] -= 1
#         elif data == "4":
#             if not user_data[id_user]['dishes']:
#                 user_data[id_user]['dishes'] = True
#                 user_data[id_user]['price'] += 10
#                 user_data[id_user]['cleaning_time'] += 0.5
#             else:
#                 user_data[id_user]['dishes'] = False
#                 user_data[id_user]['price'] -= 10
#                 user_data[id_user]['cleaning_time'] -= 0.5
#         elif data == "5":
#             if not user_data[id_user]['microwave']:
#                 user_data[id_user]['microwave'] = True
#                 user_data[id_user]['price'] += 20
#                 user_data[id_user]['cleaning_time'] += 0.5
#             else:
#                 user_data[id_user]['microwave'] = False
#                 user_data[id_user]['price'] -= 20
#                 user_data[id_user]['cleaning_time'] -= 0.5
#
#         if user_data[id_user]['refrigerator']:
#             additional_markup.add(types.InlineKeyboardButton("Внутри холодильника✅", callback_data="41"))
#         else:
#             additional_markup.add(types.InlineKeyboardButton("Внутри холодильника", callback_data="41"))
#
#         if user_data[id_user]['oven']:
#             additional_markup.add(types.InlineKeyboardButton("Внутри духовки✅", callback_data="42"))
#         else:
#             additional_markup.add(types.InlineKeyboardButton("Внутри духовки", callback_data="42"))
#
#         if user_data[id_user]['boxes']:
#             additional_markup.add(types.InlineKeyboardButton("Внутри кухонных шкафов✅", callback_data="43"))
#         else:
#             additional_markup.add(types.InlineKeyboardButton("Внутри кухонных шкафов", callback_data="43"))
#
#         if user_data[id_user]['dishes']:
#             additional_markup.add(types.InlineKeyboardButton("Помоем посуду✅", callback_data="44"))
#         else:
#             additional_markup.add(types.InlineKeyboardButton("Помоем посуду", callback_data="44"))
#
#         if user_data[id_user]['microwave']:
#             additional_markup.add(types.InlineKeyboardButton("Внутри микроволновки✅", callback_data="45"))
#         else:
#             additional_markup.add(types.InlineKeyboardButton("Внутри микроволновки", callback_data="45"))
#         additional_markup.add(types.InlineKeyboardButton("Далее", callback_data="50"))
#         bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                               text='Дополнительные опции:', parse_mode='HTML', reply_markup=additional_markup)
#
#     elif flag == '5':
#         if data == '0':
#             bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
#                                   text=f"""
# Дополнительные опции:
# {'\nВнутри холодильника' if user_data[id_user]['refrigerator'] else ''}{'\nВнутри духовки' if user_data[id_user]['oven'] else ''}{'\nВнутри кухонных шкафов' if user_data[id_user]['boxes'] else ''}{'\nПомоем посуду' if user_data[id_user]['dishes'] else ''}{'\nВнутри микроволновки' if user_data[id_user]['microwave'] else ''}
# """, parse_mode='HTML')
#             additional_markup = types.InlineKeyboardMarkup()
#             additional_markup.add(
#                 types.InlineKeyboardButton("-", callback_data="6c-"),
#                 types.InlineKeyboardButton("Погладим\nбельё (ч)", callback_data="6np"),
#                 types.InlineKeyboardButton("+", callback_data="6c+"))
#
#             additional_markup.add(
#                 types.InlineKeyboardButton("-", callback_data="6w-"),
#                 types.InlineKeyboardButton("Помоем\nокна (шт)", callback_data="6np"),
#                 types.InlineKeyboardButton("+", callback_data="6w+"))
#
#             additional_markup.add(
#                 types.InlineKeyboardButton("-", callback_data="6b-"),
#                 types.InlineKeyboardButton("Уберём на\nбалконе (шт)", callback_data="6np"),
#                 types.InlineKeyboardButton("+", callback_data="6b+"))
#
#             additional_markup.add(types.InlineKeyboardButton("Далее", callback_data="6or"))
#             bot.send_message(id_user, "Дополнительные опции:", parse_mode='HTML', reply_markup=additional_markup)
#
#     elif flag == '6':
#         if data == "c-" and user_data[id_user]['linen'] > 0:
#             user_data[id_user]['linen'] -= 1
#             user_data[id_user]['price'] -= 20
#             second_message_text(call)
#         elif data == "c+" and user_data[id_user]['linen'] < 11:
#             user_data[id_user]['linen'] += 1
#             user_data[id_user]['price'] += 20
#             second_message_text(call)
#         elif data == "w-" and user_data[id_user]['windows'] > 0:
#             user_data[id_user]['windows'] -= 1
#             user_data[id_user]['price'] -= 15
#             second_message_text(call)
#         elif data == "w+" and user_data[id_user]['windows'] < 15:
#             user_data[id_user]['windows'] += 1
#             user_data[id_user]['price'] += 15
#             second_message_text(call)
#         elif data == "b-" and user_data[id_user]['balcony'] > 0:
#             user_data[id_user]['balcony'] -= 1
#             user_data[id_user]['price'] -= 20
#             second_message_text(call)
#         elif data == "b+" and user_data[id_user]['balcony'] < 6:
#             user_data[id_user]['balcony'] += 1
#             user_data[id_user]['price'] += 20
#             second_message_text(call)
#         elif data == "np":
#             pass
#         elif data == "or":
#             text = 'Дополнительные опции:\n'
#             if user_data[id_user]['linen']:
#                 text += f'\nПогладим белье - {user_data[id_user]['linen']} ч'
#             if user_data[id_user]['windows']:
#                 text += f'\nПомоем окна - {user_data[id_user]['windows']} шт'
#             if user_data[id_user]['balcony']:
#                 text += f'\nУберём на балконе - {user_data[id_user]['balcony']} шт'
#             bot.edit_message_text(chat_id=id_user, message_id=call.message.message_id,
#                                   text=text)
#             bot.send_message(id_user,"Введите свой адрес в формате:\n<em>Адрес: Улица, Дом, Корпус, Квартира</em>",
#                              parse_mode='HTML')
#             print(user_data)
#
#
#
# print("Ready")
# bot.infinity_polling()
#
#
#
#
#
#
# # import gspread
# # import telebot
# # from telebot import types
# # from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
# # from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
# #
# # bot = telebot.TeleBot('6510684394:AAFsvSNzEk8GYqfRjRnO6N6WSsMMWWhi3Ic')
# #
# #
# # @bot.message_handler(func=lambda message: True)
# # def echo_message(message):
# #     if message.text == "/start":
# #         time_markup = types.InlineKeyboardMarkup()
# #         for i in range(9, 19):
# #             time_markup.add(types.InlineKeyboardButton(f"{str(i)+':00'}", callback_data=f"2{str(i)+':00'}"))
# #             time_markup.add(types.InlineKeyboardButton(f"{str(i) + ':30'}", callback_data=f"2{str(i) + ':30'}"))
# #
# #         bot.send_message(message.chat.id, "Выберите время:", parse_mode='HTML', reply_markup=time_markup)
# #
# #
# # print("Ready")
# # bot.infinity_polling()
#
#
#
#
#
#
#
#
# # # import telegramcalendar
# # #
# # # import config
# #
# #
# # # def on_calendar(update: Update, context: CallbackContext):
# # #     update.message.reply_text(
# # #         "Please select a date: ",
# # #         reply_markup=telegramcalendar.create_calendar()
# # #     )
# #
# #
# # # def on_callback_query(update: Update, context: CallbackContext):
# # #     query = update.callback_query
# # #     query.answer()
# # #
# # #     bot = context.bot
# # #
# # #     selected, date = telegramcalendar.process_calendar_selection(bot, update)
# # #     if selected:
# # #         query.message.reply_text(
# # #             text="You selected %s" % (date.strftime("%d/%m/%Y")),
# # #             reply_markup=ReplyKeyboardRemove()
# # #         )
# # #
# # #
# # # def main():
# # #     updater = Updater(
# # #         config.TOKEN,
# # #         use_context=True
# # #     )
# # #
# # #     dp = updater.dispatcher
# # #
# # #     dp.add_handler(CommandHandler('calendar', on_calendar))
# # #     dp.add_handler(CallbackQueryHandler(on_callback_query))
# # #
# # #     updater.start_polling()
# # #
# # #     updater.idle()
# # #
# # #
# # # if __name__ == '__main__':
# # #     main()
# # #
# # #
# # #
# # #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# #
# # # user_data = {1: {'r': 1, 'b': 5}, 2: {'r': 2, 'b': 4}}
# # #
# # #
# # # def first_message_maker(user_id):
# # #     message = ""
# # #     for key, value in user_data[user_id].items():
# # #         print(key, value)
# # #         if key == 'r':
# # #             if value == 1:
# # #                 message += "1 комната"
# # #             elif 2 <= value < 5:
# # #                 message += f"{str(value)} комнаты"
# # #             else:
# # #                 message += f"{str(value)} комнат"
# # #             message += ", "
# # #
# # #         if key == 'b':
# # #             if value == 1:
# # #                 message += "1 санузел"
# # #             elif 2 <= value < 5:
# # #                 message += f"{str(value)} санузла"
# # #             else:
# # #                 message += f"{str(value)} санузлов"
# # #             message += "."
# # #
# # #     return message
# # #
# # #
# # # print(first_message_maker(1))
# # # print()
# # # # print(first_message_maker(2))
# # # # print()
# # #
# # # for key, value in user_data[1].items(): print(key, value)
# # #
# # # # import gspread
# # # # import telebot
# # # # from telebot import types
# # # # from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaPhoto
# # # #
# # # #
# # # # bot = telebot.TeleBot('6510684394:AAFsvSNzEk8GYqfRjRnO6N6WSsMMWWhi3Ic')
# # # #
# # # # @bot.message_handler(commands=['start'])
# # # # def start_msg(message):
# # # # 	keyboard = types.InlineKeyboardMarkup(row_width=1)
# # # # 	one = types.InlineKeyboardButton('1', callback_data='one')
# # # # 	two = types.InlineKeyboardButton('2', callback_data='two')
# # # # 	three = types.InlineKeyboardButton('3', callback_data='three')
# # # # 	keyboard.add(one, two, three)
# # # # 	bot.send_message(message.chat.id, 'AgACAgIAAxkDAAIB5GC-NXY5xQjMHR-sYdvZ9iqHGj38AAIKtTEbV1nxSQW3xZ3j3DnT-Eo0ny4AAwEAAwIAA3kAA58GBQABHwQ', reply_markup=keyboard)
# # # #
# # # #
# # # # #обработка callback клавиатуры
# # # # @bot.callback_query_handler(func=lambda message: True)
# # # # def logic_inline(call):
# # # # 	if call.data == 'one':
# # # # 		  bot.edit_message_caption(chat_id=call.message.chat.id, message_id=call.message.message_id, caption='Ты нажал на кнопку 1')
# # # #
# # # #
# # # # print("Ready")
# # # # bot.infinity_polling()
