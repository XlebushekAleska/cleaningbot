import telebot
from telebot import types
from telegram_bot_calendar import DetailedTelegramCalendar, LSTEP
from datetime import datetime, timedelta
from adminbot import handle_admin_messages, handle_admin_callback
from workerbot import handle_worker_messages, handle_worker_callback
from db_class import Database

# Создание объекта базы данных
db = Database("Database1.db")
# admins_list = db.own_query("SELECT telegram_id from Users WHERE role = 'admin'")[0]
# workers_list = db.own_query("SELECT telegram_id from Users WHERE role = 'employee'")[0]
bot = telebot.TeleBot('6510684394:AAFsvSNzEk8GYqfRjRnO6N6WSsMMWWhi3Ic')
workers_list = []
admins_list = [769963229]
# 769963229
user_data = {}
user_review = {}

last_message_list = [
    'Количество комнат: ',
    'Количество санузлов: ',
    'Стоимость (BYN): ',
    'Скидка: ',
    'Длительность уборки (ч): ',
    'Дата: ',
    'Время: ',
    'Внутри холодильника: ',
    'Внутри Духовки: ',
    'Внутри кухонных шкафов: ',
    'Помоем посуду: ',
    'Внутри микроволновки: ',
    'Погладим бельё (ч): ',
    'Помоем окна (шт): ',
    'Уберём на балконе (шт):',
    'Улица:',
    'Дом: ',
    'Корпус: ',
    'Квартира: ',
    'Имя: ',
    'Фамилия: ',
    'Отчество: ',
    'Номер телефона: ',
    'email: ',
]


def first_message_maker(user_id):
    global user_data
    rooms_price = 0.0
    bathrooms_price = 0.0
    rooms_time = 0.0
    bathrooms_time = 0.0
    message = ""
    for key, value in user_data[user_id].items():
        if key == 'rooms':
            if value == 1:
                message += "1 комната"
            elif 2 <= value < 5:
                message += f"{str(value)} комнаты"
            else:
                message += f"{str(value)} комнат"
            message += ", "
            rooms_price = value * 14
            rooms_time = value
        if key == 'bathrooms':
            if value == 1:
                message += "1 санузел"
            elif 2 <= value < 5:
                message += f"{str(value)} санузла"
            else:
                message += f"{str(value)} санузлов"
            message += "."
            bathrooms_price = value * 20
            bathrooms_time = value * 0.5

    user_data[user_id]['price'] = 31 + rooms_price + bathrooms_price
    user_data[user_id]['cleaning_time'] = 2 + rooms_time + bathrooms_time
    return message


# функция, генерирующая приветственное сообщение
def zero_message_text(call=None, message=None):
    if call:
        id_user = call.message.chat.id
    else:
        id_user = message.chat.id
    text = f"""
Добро пожаловать в бота-ассистента
клининговой компании <a href='https://t.me/cleanny_by'><b>"КлинниБогинни"!</b></a>

Я помогу Вам ознакомиться со списком услуг,
рассчитать стоимость заказа, а также 
посмотреть и оставить отзывы о нашей компании!

Выберите необходимую опцию ниже:
       
"""
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Заказать уборку", callback_data="01"))
    markup.add(types.InlineKeyboardButton("Отзывы", callback_data="02"))

    if call:
        # Редактирование текста сообщения и обновление клавиатуры
        bot.edit_message_text(chat_id=id_user, message_id=call.message.message_id,
                              text=text, parse_mode='HTML', reply_markup=markup)
    else:
        bot.send_message(chat_id=id_user,
                         text=text, parse_mode='HTML', reply_markup=markup)


def first_message_text(call=None, message=None):
    if call:
        id_user = call.message.chat.id
    else:
        id_user = message.chat.id
    text = f"""
Для изменения основных параметров заказа
воспользуйтесь клавиатурой ниже. 

<a href="https://drive.google.com/file/d/1gH8ogErgeWSeqIPhM9XQVPitbmzHxG1v/view">Из чего состоит базовая уборка: чек-лист</a>

Ваш заказвключает в себя сейчас:

{first_message_maker(id_user)}
<b>{user_data[id_user]['price']}BYN.</b>

<em>1 санузел = 1 ванная + 1 туалет
(неважно, совмещенные или раздельные)
Кухня и коридор включены в стоимость.</em>        
"""
    markup = types.InlineKeyboardMarkup()
    markup.add(
        types.InlineKeyboardButton("-", callback_data="1r-"),
        types.InlineKeyboardButton("комната", callback_data="1np"),
        types.InlineKeyboardButton("+", callback_data="1r+"))
    markup.add(
        types.InlineKeyboardButton("-", callback_data="1b-"),
        types.InlineKeyboardButton("санузел", callback_data="1np"),
        types.InlineKeyboardButton("+", callback_data="1b+"))
    markup.add(types.InlineKeyboardButton("Рассчитать уборку", callback_data="1or"))

    if call:
        # Редактирование текста сообщения и обновление клавиатуры
        bot.edit_message_text(chat_id=id_user, message_id=call.message.message_id,
                              text=text, parse_mode='HTML', reply_markup=markup)
    else:
        bot.send_message(chat_id=id_user,
                         text=text, parse_mode='HTML', reply_markup=markup)


def second_message_text(call):
    id_user = call.message.chat.id
    text = f"Дополнительные опции:\n"

    if user_data[id_user]['linen']:
        text += f'\nПогладим белье - {user_data[id_user]['linen']} ч'
    if user_data[id_user]['windows']:
        text += f'\nПомоем окна - {user_data[id_user]['windows']} шт'
    if user_data[id_user]['balcony']:
        text += f'\nУберём на балконе - {user_data[id_user]['balcony']} шт'

    additional_markup = types.InlineKeyboardMarkup()
    additional_markup.add(
        types.InlineKeyboardButton("-", callback_data="6c-"),
        types.InlineKeyboardButton("Погладим\nбельё (ч)", callback_data="6np"),
        types.InlineKeyboardButton("+", callback_data="6c+"))

    additional_markup.add(
        types.InlineKeyboardButton("-", callback_data="6w-"),
        types.InlineKeyboardButton("Помоем\nокна (шт)", callback_data="6np"),
        types.InlineKeyboardButton("+", callback_data="6w+"))

    additional_markup.add(
        types.InlineKeyboardButton("-", callback_data="6b-"),
        types.InlineKeyboardButton("Уберём на\nбалконе (шт)", callback_data="6np"),
        types.InlineKeyboardButton("+", callback_data="6b+"))

    additional_markup.add(types.InlineKeyboardButton("Далее", callback_data="6or"))

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text, parse_mode='HTML', reply_markup=additional_markup)


def last_message_text(message):
    text = '<b>Ваша уборка:</b>\n'
    rooms_text = '\n<em><b>Количество комнат: </b></em>'
    price_text = '\n<em><b>Стоимость: </b></em>'
    aditional_text = '\n<em><b>Дополнительные услуги: </b></em>'
    adress_text = '\n<em><b>Адрес и контактная информация: </b></em>'
    for index, (key, value) in enumerate(user_data[message.chat.id].items()):
        if value:
            if key in ['rooms', 'bathrooms']:
                rooms_text += f'\n{last_message_list[index]}{str(value if str(value) != 'True' else '✅')}'
            elif key in ['price', 'time', 'date', 'cleaning_time']:
                price_text += f'\n{last_message_list[index]}{str(value if str(value) != 'True' else '✅')}'
            elif key in ['refrigerator', 'oven', 'boxes', 'dishes', 'microwave', 'linen', 'windows', 'balcony']:
                aditional_text += f'\n{last_message_list[index]}{str(value if str(value) != 'True' else '✅')}'
            elif key in ['street', 'house', 'body', 'apartment', 'first_name', 'second_name', 'third_name',
                         'phone_number', 'email']:
                adress_text += f'\n{last_message_list[index]}{str(value if str(value) != 'True' else '✅')}'
    now = datetime.now()
    last_month = now - timedelta(days=31)
    # Преобразуем даты в строки формата "YYYY-MM-DD"
    now_str = now.strftime('%Y-%m-%d')
    last_month_str = last_month.strftime('%Y-%m-%d')
    # Запрос для получения количества заказов за последние 31 день
    discount_reason = db.own_query(f"""
        SELECT count(id) 
        FROM Orders 
        WHERE order_date BETWEEN '{last_month_str}' AND '{now_str}'
    """)[0][0]
    discount = 0
    regularity = '1 раз или первый раз'
    price = user_data[message.chat.id]['price']
    if discount_reason >= 4:
        discount = 15
        regularity = 'Раз в неделю'
    elif discount_reason >= 2:
        discount = 10
        regularity = 'Раз в две недели'
    elif discount_reason == 1:
        discount = 7
        regularity = 'Раз в месяц'
    user_data[message.chat.id]['discount'] = discount
    discount_price = price * (100 - discount) / 100
    text += (f'{rooms_text}\n{aditional_text}'
             f'\n{adress_text}\n{price_text}\n'
             f'\nРегулярность: {regularity}\n'
             f'Скидка за регулярность: {discount}\n'
             f'Сумма скидки за регулярность: {price * discount / 100}\n'
             f'К оплате: {discount_price}\n'
             )
    text += ('\nНажимая кнопку «Заказать уборку», вы соглашаетесь с \n'
             '<a href="https://cleanny.by/licence">«Договором – публичной офертой на оказание клининговых '
             'услуг»</a> и '
             '<a href="https://cleanny.by/privacy">«Политикой по сбору и обработке персональных данных '
             'ресурсов»</a>'
             )
    return text


@bot.callback_query_handler(func=DetailedTelegramCalendar.func())
def cal(c):
    result, key, step = DetailedTelegramCalendar().process(c.data)
    if not result and key:
        # Select {LSTEP[step]}
        bot.edit_message_text(f"Выберите дату:",
                              c.message.chat.id,
                              c.message.message_id,
                              reply_markup=key)
    elif result:
        if result < datetime.now().date() + timedelta(days=1):
            tomorrow = datetime.now().date() + timedelta(days=1)
            calendar, step = DetailedTelegramCalendar(min_date=tomorrow).build()
            bot.edit_message_text(f"Выберите корректную дату\n(начиная с {tomorrow})",
                                  c.message.chat.id,
                                  c.message.message_id,
                                  reply_markup=calendar
                                  )
        else:
            bot.edit_message_text(f"Дата уборки: {result}",
                                  c.message.chat.id,
                                  c.message.message_id)
            global user_data
            user_data[c.from_user.id]['date'] = result
            time_markup = types.InlineKeyboardMarkup()
            for i in range(9, 19):
                time_markup.add(types.InlineKeyboardButton(f"{str(i) + ':00'}", callback_data=f"2{str(i) + ':00'}"))
                time_markup.add(types.InlineKeyboardButton(f"{str(i) + ':30'}", callback_data=f"2{str(i) + ':30'}"))
            bot.send_message(c.message.chat.id, "Выберите время:", parse_mode='HTML', reply_markup=time_markup)


# Обработчик текстовых сообщений
@bot.message_handler(func=lambda message: True)
def echo_message(message):
    # print(message)
    if message.chat.id in admins_list:
        handle_admin_messages(bot, message)  # Передаем управление на админский функционал
    elif message.chat.id in workers_list:
        handle_worker_messages(bot, message)  # Передаем управление на функционал для работников
    else:
        if message.text == "/start":
            if message.chat.id not in user_data:
                user_data[message.chat.id] = {
                    'rooms': 1,
                    'bathrooms': 1,
                    'price': 31,
                    'discount': 0,
                    'cleaning_time': 2,
                    'date': '',
                    'time': '',
                    'refrigerator': False,
                    'oven': False,
                    'boxes': False,
                    'dishes': False,
                    'microwave': False,
                    'linen': 0,
                    'windows': 0,
                    'balcony': 0,
                    'street': '',
                    'house': '',
                    'body': '',
                    'apartment': '',
                    'first_name': '',
                    'second_name': '',
                    'third_name': '',
                    'phone_number': '',
                    'email': '',
                }

            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton("-", callback_data="1r-"),
                types.InlineKeyboardButton("комната", callback_data="1np"),
                types.InlineKeyboardButton("+", callback_data="1r+"))

            markup.add(
                types.InlineKeyboardButton("-", callback_data="1b-"),
                types.InlineKeyboardButton("санузел", callback_data="1np"),
                types.InlineKeyboardButton("+", callback_data="1b+"))

            markup.add(types.InlineKeyboardButton("Рассчитать уборку", callback_data="1or"))

            zero_message_text(message=message)

        elif 'Адрес' in message.text:
            if user_data[message.chat.id]['time'] != '':
                try:
                    adress = message.text[message.text.index(":") + 1:].split(', ')
                    user_data[message.chat.id]['street'] = adress[0]
                    user_data[message.chat.id]['house'] = adress[1]
                    user_data[message.chat.id]['body'] = adress[2]
                    user_data[message.chat.id]['apartment'] = adress[3]
                    bot.send_message(message.chat.id,
                                     "Введите своё ФИО в формате:\n<em>ФИО: Фамилия Имя Отчество</em>",
                                     parse_mode='HTML')

                except:
                    bot.send_message(message.chat.id,
                                     "<b>Вводите данные исключительно согласно образцу!</b>",
                                     parse_mode='HTML')
            else:
                bot.send_message(message.chat.id,
                                 "<b>Вводите исключительно требуемые данные!</b>",
                                 parse_mode='HTML')
        elif 'ФИО' in message.text:
            if user_data[message.chat.id]['street'] != '':
                try:
                    name = message.text[message.text.index(":") + 2:].split(' ')
                    user_data[message.chat.id]['second_name'] = name[0]
                    user_data[message.chat.id]['first_name'] = name[1]
                    user_data[message.chat.id]['third_name'] = name[2]
                    bot.send_message(message.chat.id,
                                     "Введите свои контакты в формате:\n<em>Контакты: номер телефона, email</em>",
                                     parse_mode='HTML')
                except:
                    bot.send_message(message.chat.id,
                                     "<b>Вводите данные исключительно согласно образцу!</b>",
                                     parse_mode='HTML')
            else:
                bot.send_message(message.chat.id,
                                 "<b>Вводите исключительно требуемые данные!</b>",
                                 parse_mode='HTML')
        elif 'Контакты' in message.text:
            if user_data[message.chat.id]['first_name'] != '':
                try:
                    contacts = message.text[message.text.index(":") + 1:].split(', ')
                    user_data[message.chat.id]['phone_number'] = contacts[0]
                    user_data[message.chat.id]['email'] = contacts[1]

                except:
                    bot.send_message(message.chat.id,
                                     "<b>Вводите данные исключительно согласно образцу!</b>",
                                     parse_mode='HTML')

                text = last_message_text(message)
                final_markup = types.InlineKeyboardMarkup()
                final_markup.add(types.InlineKeyboardButton("Заказать уборку", callback_data="f0"))
                bot.send_message(message.chat.id,
                                 text=text,
                                 parse_mode='HTML',
                                 reply_markup=final_markup
                                 )
            else:
                bot.send_message(message.chat.id,
                                 "<b>Вводите исключительно требуемые данные!</b>",
                                 parse_mode='HTML')

        elif message.text[:6] == 'Отзыв:':
            if user_review[message.chat.id] != {}:
                try:
                    comment = message.text[6:]
                    user_id = db.own_query(f'SELECT id FROM Users WHERE telegram_id={message.chat.id}')[0][0]
                    db.set_data('Feedback', [
                        user_id,
                        user_review[message.chat.id]['order_id'],
                        user_review[message.chat.id]['rating'],
                        comment
                    ])
                    user_review[message.chat.id] = {}
                    bot.send_message(message.chat.id, 'Ваш отзыв записан. Спасибо, что оставили Ваш отзыв!')
                    zero_message_text(message=message)
                except:
                    bot.send_message(message.chat.id,
                                     "<b>Вводите данные исключительно согласно образцу!</b>",
                                     parse_mode='HTML')
            else:
                bot.send_message(message.chat.id,
                                 "<b>Вводите требуемые данные!</b>",
                                 parse_mode='HTML')

        else:
            bot.send_message(message.chat.id,
                             "<b>Вводите данные исключительно согласно образцу!</b>",
                             parse_mode='HTML')


@bot.callback_query_handler(func=lambda call: True)
def query_handler(call):
    if call.message.chat.id in admins_list:
        handle_admin_callback(bot, call)
    elif call.message.chat.id in workers_list:
        handle_worker_callback(bot, call)
    else:
        bot.answer_callback_query(callback_query_id=call.id, )
        id_user = call.message.chat.id
        flag = call.data[0:1]
        data = call.data[1:]
        if flag == '0':
            if data == '0':
                zero_message_text(call=call)
            elif data == '1':
                first_message_text(call=call)
            elif data == '2':
                feedback_markup = types.InlineKeyboardMarkup()
                feedback_markup.add(types.InlineKeyboardButton("Перейти к отзывам", callback_data="03"))
                feedback_markup.add(types.InlineKeyboardButton("Оставить свой отзыв", callback_data="04"))
                feedback_markup.add(types.InlineKeyboardButton("В начало", callback_data="00"))
                bot.edit_message_text(chat_id=id_user, message_id=call.message.message_id,
                                      text='Это отдел отзывов.\nТут Вы можете ознакомиться с отзывами наших клиентов, '
                                           'а также оставить свои.',
                                      reply_markup=feedback_markup)

            elif data[0] == '3':

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
                    review_markup.add(
                        types.InlineKeyboardButton("◀", callback_data=f"03{index}-"),
                        types.InlineKeyboardButton("▶", callback_data=f"03{index}+")
                    )
                    review_markup.add(types.InlineKeyboardButton("Назад", callback_data=f"02"))
                    return review_markup

                feedback = db.own_query('SELECT * FROM Feedback WHERE rating >= 3')
                feedback_list = [
                    f"{''.join('★' * review[3] + '☆' * (5 - review[3]))}\n\nОтзыв: \n{review[4]}" for review in feedback
                ]

                if len(data) == 1:
                    bot.edit_message_text(chat_id=id_user, message_id=call.message.message_id,
                                          text=feedback_list[0],
                                          reply_markup=get_review_markup(0))
                else:
                    direction = data[-1]
                    current_index = int(data[1:-1])
                    gen = review_index_generator(current_index,
                                                 direction)  # Используем генератор для получения нового индекса
                    new_index = next(gen)

                    if new_index < 0:
                        new_index = len(feedback_list) - 1
                    elif new_index >= len(feedback_list):
                        new_index = 0

                    # Изменяем сообщение только если новый индекс отличается от текущего
                    if new_index != current_index:
                        bot.edit_message_text(chat_id=id_user, message_id=call.message.message_id,
                                              text=feedback_list[new_index],
                                              reply_markup=get_review_markup(new_index))

            elif data[0] == '4':

                def review_index_generator(start, direction):
                    index = start
                    while True:
                        if direction == '+':
                            index += 1
                        elif direction == '-':
                            index -= 1
                        yield index

                def get_review_markup(index, chunked_orders_list):
                    review_markup = types.InlineKeyboardMarkup()
                    for order in chunked_orders_list[index]:
                        review_markup.add(
                            types.InlineKeyboardButton(text=order['cleaning_date'], callback_data=f"05{order['id']}"))

                    review_markup.add(
                        types.InlineKeyboardButton("◀", callback_data=f"04{index}-"),
                        types.InlineKeyboardButton("▶", callback_data=f"04{index}+")
                    )
                    review_markup.add(types.InlineKeyboardButton("Назад", callback_data=f"02"))
                    return review_markup

                now = (datetime.now().date() + timedelta(days=5550))
                user_id = db.own_query(f'SELECT id FROM Users WHERE telegram_id={id_user}')[0][0]
                orders_list = db.own_query(f"SELECT id, cleaning_date "
                                           f"FROM Orders "
                                           f"WHERE user_id={user_id} "
                                           f"AND cleaning_date < '{now}'"
                                           )

                # Преобразуем список заказов в список словарей
                orders_dict_list = [{'id': order[0], 'cleaning_date': order[1]} for order in orders_list]

                # Разбиваем список на подмножества (страницы)
                chunked_orders_list = [orders_dict_list[i:i + 3] for i in range(0, len(orders_dict_list), 3)]

                if len(data) == 1:
                    bot.edit_message_text(chat_id=id_user, message_id=call.message.message_id,
                                          text="Выберите дату заказа, к которому хотите оставить отзыв",
                                          reply_markup=get_review_markup(0, chunked_orders_list)
                                          )
                else:
                    direction = data[-1]
                    current_index = int(data[1:-1])
                    gen = review_index_generator(current_index, direction)
                    new_index = next(gen)

                    # Убедитесь, что индекс не выходит за пределы списка
                    if new_index < 0:
                        new_index = len(chunked_orders_list) - 1
                    elif new_index >= len(chunked_orders_list):
                        new_index = 0

                    # Изменяем сообщение только если новый индекс отличается от текущего
                    if new_index != current_index:
                        bot.edit_message_text(chat_id=id_user, message_id=call.message.message_id,
                                              text="Выберите дату заказа, к которому хотите оставить отзыв",
                                              reply_markup=get_review_markup(new_index, chunked_orders_list))

            elif data[0] == '5':
                user_review[id_user] = {}
                order_id = data[1:]
                user_review[id_user]['order_id'] = order_id
                rating_markup = types.InlineKeyboardMarkup()
                rating_markup.add(types.InlineKeyboardButton("★☆☆☆☆", callback_data="061"))
                rating_markup.add(types.InlineKeyboardButton("★★☆☆☆", callback_data="062"))
                rating_markup.add(types.InlineKeyboardButton("★★★☆☆", callback_data="063"))
                rating_markup.add(types.InlineKeyboardButton("★★★★☆", callback_data="064"))
                rating_markup.add(types.InlineKeyboardButton("★★★★★", callback_data="065"))
                bot.edit_message_text(chat_id=id_user, message_id=call.message.message_id,
                                      text=f"Оцените заказ от {data}",
                                      reply_markup=rating_markup
                                      )
            elif data[0] == '6':
                user_review[id_user]['rating'] = data[-1]
                bot.edit_message_text(chat_id=id_user, message_id=call.message.message_id,
                                      text=f"Отправьте Ваш отзыв, указав в начале:\n<b>Отзыв:</b>",
                                      parse_mode='HTML'
                                      )

        elif flag == '1':
            if data == "r-" and user_data[id_user]['rooms'] > 1:
                user_data[id_user]['rooms'] -= 1
                first_message_text(call=call)
            elif data == "r+" and user_data[id_user]['rooms'] < 10:
                user_data[id_user]['rooms'] += 1
                first_message_text(call=call)
            elif data == "b-" and user_data[id_user]['bathrooms'] > 1:
                user_data[id_user]['bathrooms'] -= 1
                first_message_text(call=call)
            elif data == "b+" and user_data[id_user]['bathrooms'] < 10:
                user_data[id_user]['bathrooms'] += 1
                first_message_text(call=call)
            elif data == "np":
                pass
            elif data == "or":
                tomorrow = datetime.now().date() + timedelta(days=1)
                calendar, step = DetailedTelegramCalendar(min_date=tomorrow).build()
                bot.send_message(id_user,
                                 f"Select {LSTEP[step]}",
                                 reply_markup=calendar)

        elif flag == '2':
            user_data[id_user]['time'] = data
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text=f'Время: {data}', parse_mode='HTML')

            additional_markup = types.InlineKeyboardMarkup()
            additional_markup.add(types.InlineKeyboardButton("Внутри холодильника", callback_data="41"))
            additional_markup.add(types.InlineKeyboardButton("Внутри духовки", callback_data="42"))
            additional_markup.add(types.InlineKeyboardButton("Внутри кухонных шкафов", callback_data="43"))
            additional_markup.add(types.InlineKeyboardButton("Помоем посуду", callback_data="44"))
            additional_markup.add(types.InlineKeyboardButton("Внутри микроволновки", callback_data="45"))
            additional_markup.add(types.InlineKeyboardButton("Далее", callback_data="50"))
            bot.send_message(id_user, "Дополнительные опции:", parse_mode='HTML', reply_markup=additional_markup)

        elif flag == '4':
            additional_markup = types.InlineKeyboardMarkup()
            if data == "1":
                if not user_data[id_user]['refrigerator']:
                    user_data[id_user]['refrigerator'] = True
                    user_data[id_user]['price'] += 25
                    user_data[id_user]['cleaning_time'] += 1
                else:
                    user_data[id_user]['refrigerator'] = False
                    user_data[id_user]['price'] -= 25
                    user_data[id_user]['cleaning_time'] -= 1
            elif data == "2":
                if not user_data[id_user]['oven']:
                    user_data[id_user]['oven'] = True
                    user_data[id_user]['price'] += 25
                    user_data[id_user]['cleaning_time'] += 1
                else:
                    user_data[id_user]['oven'] = False
                    user_data[id_user]['price'] -= 25
                    user_data[id_user]['cleaning_time'] -= 1
            elif data == "3":
                if not user_data[id_user]['boxes']:
                    user_data[id_user]['boxes'] = True
                    user_data[id_user]['price'] += 25
                    user_data[id_user]['cleaning_time'] += 1
                else:
                    user_data[id_user]['boxes'] = False
                    user_data[id_user]['price'] -= 25
                    user_data[id_user]['cleaning_time'] -= 1
            elif data == "4":
                if not user_data[id_user]['dishes']:
                    user_data[id_user]['dishes'] = True
                    user_data[id_user]['price'] += 10
                    user_data[id_user]['cleaning_time'] += 0.5
                else:
                    user_data[id_user]['dishes'] = False
                    user_data[id_user]['price'] -= 10
                    user_data[id_user]['cleaning_time'] -= 0.5
            elif data == "5":
                if not user_data[id_user]['microwave']:
                    user_data[id_user]['microwave'] = True
                    user_data[id_user]['price'] += 20
                    user_data[id_user]['cleaning_time'] += 0.5
                else:
                    user_data[id_user]['microwave'] = False
                    user_data[id_user]['price'] -= 20
                    user_data[id_user]['cleaning_time'] -= 0.5

            if user_data[id_user]['refrigerator']:
                additional_markup.add(types.InlineKeyboardButton("Внутри холодильника✅", callback_data="41"))
            else:
                additional_markup.add(types.InlineKeyboardButton("Внутри холодильника", callback_data="41"))

            if user_data[id_user]['oven']:
                additional_markup.add(types.InlineKeyboardButton("Внутри духовки✅", callback_data="42"))
            else:
                additional_markup.add(types.InlineKeyboardButton("Внутри духовки", callback_data="42"))

            if user_data[id_user]['boxes']:
                additional_markup.add(types.InlineKeyboardButton("Внутри кухонных шкафов✅", callback_data="43"))
            else:
                additional_markup.add(types.InlineKeyboardButton("Внутри кухонных шкафов", callback_data="43"))

            if user_data[id_user]['dishes']:
                additional_markup.add(types.InlineKeyboardButton("Помоем посуду✅", callback_data="44"))
            else:
                additional_markup.add(types.InlineKeyboardButton("Помоем посуду", callback_data="44"))

            if user_data[id_user]['microwave']:
                additional_markup.add(types.InlineKeyboardButton("Внутри микроволновки✅", callback_data="45"))
            else:
                additional_markup.add(types.InlineKeyboardButton("Внутри микроволновки", callback_data="45"))
            additional_markup.add(types.InlineKeyboardButton("Далее", callback_data="50"))
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text='Дополнительные опции:', parse_mode='HTML', reply_markup=additional_markup)

        elif flag == '5':
            if data == '0':
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=f"""
Дополнительные опции:
{'\nВнутри холодильника' if user_data[id_user]['refrigerator'] else ''}{'\nВнутри духовки' if user_data[id_user]['oven'] else ''}{'\nВнутри кухонных шкафов' if user_data[id_user]['boxes'] else ''}{'\nПомоем посуду' if user_data[id_user]['dishes'] else ''}{'\nВнутри микроволновки' if user_data[id_user]['microwave'] else ''}
""", parse_mode='HTML')
                additional_markup = types.InlineKeyboardMarkup()
                additional_markup.add(
                    types.InlineKeyboardButton("-", callback_data="6c-"),
                    types.InlineKeyboardButton("Погладим\nбельё (ч)", callback_data="6np"),
                    types.InlineKeyboardButton("+", callback_data="6c+"))

                additional_markup.add(
                    types.InlineKeyboardButton("-", callback_data="6w-"),
                    types.InlineKeyboardButton("Помоем\nокна (шт)", callback_data="6np"),
                    types.InlineKeyboardButton("+", callback_data="6w+"))

                additional_markup.add(
                    types.InlineKeyboardButton("-", callback_data="6b-"),
                    types.InlineKeyboardButton("Уберём на\nбалконе (шт)", callback_data="6np"),
                    types.InlineKeyboardButton("+", callback_data="6b+"))

                additional_markup.add(types.InlineKeyboardButton("Далее", callback_data="6or"))
                bot.send_message(id_user, "Дополнительные опции:", parse_mode='HTML', reply_markup=additional_markup)

        elif flag == '6':
            if data == "c-" and user_data[id_user]['linen'] > 0:
                user_data[id_user]['linen'] -= 1
                user_data[id_user]['price'] -= 20
                second_message_text(call)
            elif data == "c+" and user_data[id_user]['linen'] < 11:
                user_data[id_user]['linen'] += 1
                user_data[id_user]['price'] += 20
                second_message_text(call)
            elif data == "w-" and user_data[id_user]['windows'] > 0:
                user_data[id_user]['windows'] -= 1
                user_data[id_user]['price'] -= 15
                second_message_text(call)
            elif data == "w+" and user_data[id_user]['windows'] < 15:
                user_data[id_user]['windows'] += 1
                user_data[id_user]['price'] += 15
                second_message_text(call)
            elif data == "b-" and user_data[id_user]['balcony'] > 0:
                user_data[id_user]['balcony'] -= 1
                user_data[id_user]['price'] -= 20
                second_message_text(call)
            elif data == "b+" and user_data[id_user]['balcony'] < 6:
                user_data[id_user]['balcony'] += 1
                user_data[id_user]['price'] += 20
                second_message_text(call)
            elif data == "np":
                pass
            elif data == "or":
                text = 'Дополнительные опции:\n'
                if user_data[id_user]['linen']:
                    text += f'\nПогладим белье - {user_data[id_user]['linen']} ч'
                if user_data[id_user]['windows']:
                    text += f'\nПомоем окна - {user_data[id_user]['windows']} шт'
                if user_data[id_user]['balcony']:
                    text += f'\nУберём на балконе - {user_data[id_user]['balcony']} шт'
                bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                      text=text)
                bot.send_message(id_user, "Введите свой адрес в формате:\n<em>Адрес: Улица, Дом, Корпус, Квартира</em>",
                                 parse_mode='HTML')

        elif flag == 'f':
            if data == '0':
                # Поиск user_id по telegram_id
                try:
                    user_id_result = db.own_query("SELECT id FROM Users WHERE telegram_id = ?", (id_user,))
                    if user_id_result:
                        user_id = user_id_result[0][0]  # Получаем user_id из результата запроса
                    else:
                        raise ValueError("User not found")  # Исключение, если пользователь не найден

                except ValueError as e:
                    if str(e) == "User not found":
                        # Добавляем пользователя в базу данных, если не найден
                        user_insert_query = """INSERT INTO Users (telegram_id, first_name, second_name, third_name, 
                        phone_number, email, role) VALUES (?, ?, ?, ?, ?, ?, ?)"""
                        # Данные для вставки
                        data = (
                            id_user,
                            user_data[id_user]['first_name'],
                            user_data[id_user]['second_name'],
                            user_data[id_user]['third_name'],
                            user_data[id_user]['phone_number'],
                            user_data[id_user]['email'],
                            'client',
                        )
                        db.own_query(user_insert_query, data, fetch=False)
                        # Получаем user_id нового пользователя
                        user_id = db.own_query("SELECT id FROM Users WHERE telegram_id = ?", (id_user,))[0][0]
                    else:
                        raise  # Перебрасываем другие ошибки

                # Запрос для вставки нового заказа
                order_insert_query = """INSERT INTO Orders (user_id, price, discount, adress, status, rooms, bathrooms, 
                cleaning_date, cleaning_time, refrigerator, oven, boxes, dishes, microwave, linen, windows, 
                balcony) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""

                adress = (f'Ул. {user_data[id_user]['street']}, д. {user_data[id_user]['house']}, к. '
                          f'{user_data[id_user]['body']}, кв. {user_data[id_user]['apartment']}')

                status = 'поступил'

                order_data = (
                    user_id,
                    user_data[id_user]['price'],
                    user_data[id_user]['discount'],
                    adress,
                    status,
                    user_data[id_user]['rooms'],
                    user_data[id_user]['bathrooms'],
                    user_data[id_user]['date'],
                    user_data[id_user]['time'],
                    user_data[id_user]['refrigerator'],
                    user_data[id_user]['oven'],
                    user_data[id_user]['boxes'],
                    user_data[id_user]['dishes'],
                    user_data[id_user]['microwave'],
                    user_data[id_user]['linen'],
                    user_data[id_user]['windows'],
                    user_data[id_user]['balcony'],
                )

                db.own_query(order_insert_query, order_data, fetch=False)

                text = last_message_text(call.message)
                text += '\n\nЗаказ оформлен ✔'
                text += ("\n\nДля изменения заказа свяжитесь с нами по номеру \n+375 (44) 711-11-85 "
                         "или в <a href='https://t.me/cleanny_by'><b>этом чате</b></a>")
                bot.edit_message_text(chat_id=id_user, message_id=call.message.message_id,
                                      text=text, parse_mode='HTML')

                user_data[id_user]['refrigerator'] = False
                user_data[id_user]['oven'] = False
                user_data[id_user]['boxes'] = False
                user_data[id_user]['dishes'] = False
                user_data[id_user]['microwave'] = False
                user_data[id_user]['linen'] = 0
                user_data[id_user]['windows'] = 0
                user_data[id_user]['balcony'] = 0
                user_data[id_user]['street'] = ''
                user_data[id_user]['house'] = ''
                user_data[id_user]['body'] = ''
                user_data[id_user]['apartment'] = ''
                user_data[id_user]['first_name'] = ''
                user_data[id_user]['second_name'] = ''
                user_data[id_user]['third_name'] = ''
                user_data[id_user]['phone_number'] = ''
                user_data[id_user]['email'] = ''


print("Ready")
bot.infinity_polling()
