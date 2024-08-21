import sqlite3


class Database:
    def __init__(self, db_name):
        self.db_name = db_name

    def __connect(self):
        conn = sqlite3.connect(self.db_name)
        cur = conn.cursor()
        return conn, cur

    def get_column_names(self, table_name: str):
        conn, cur = self.__connect()
        cur.execute(f"SELECT * FROM {table_name} LIMIT 0")
        column_names = [description[0] for description in cur.description]
        conn.close()
        return column_names

    def set_data(self, table_name: str, data: list):
        conn, cur = self.__connect()
        cur.execute(f"SELECT * FROM {table_name} LIMIT 0")
        column_names = [description[0] for description in cur.description]
        column_names.remove('id')
        if 'registration_date' in column_names:
            column_names.remove('registration_date')
        elif 'order_date' in column_names:
            column_names.remove('order_date')
        elif 'created_at' in column_names:
            column_names.remove('created_at')
        elif 'issued_at' in column_names:
            column_names.remove('issued_at')

        placeholders = ', '.join('?' for _ in range(len(data)))
        column_names = ', '.join(column_names)

        query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
        cur.execute(query, data)
        conn.commit()
        conn.close()

    def get_data(self, table_name, row_id):
        conn, cur = self.__connect()
        query = f"SELECT * FROM {table_name} WHERE id=?"
        cur.execute(query, (row_id,))
        row = cur.fetchall()[0]
        column_names = [description[0] for description in cur.description]
        conn.close()
        return row, column_names if row else None

    def delete_data(self, table_name, row_id):
        conn, cur = self.__connect()
        query = f'''DELETE FROM {table_name} WHERE id = ?'''
        cur.execute(query, (row_id,))
        conn.commit()
        conn.close()

    def change_data(self, table_name: str, row_id: int, data: dict):
        conn, cur = self.__connect()
        query = f'''UPDATE {table_name} SET\n'''
        for key, value in data.items():
            query += f'"{key}" = "{value}",\n'
        query = query[:-2] + f'\nWHERE id = {row_id}'
        cur.execute(query)
        conn.commit()
        conn.close()

    def own_query(self, query, data=None, fetch=True, columns=False):
        conn, cur = self.__connect()
        if data:
            cur.execute(query, data)
        else:
            cur.execute(query)

        if columns:
            result = []
            result_data = cur.fetchall() if fetch else None
            columns = tuple([description[0] for description in cur.description])
            result.append(columns)
            result.append(result_data)

        else:
            result = cur.fetchall() if fetch else None
        conn.commit()
        conn.close()
        return result


# db = Database('Database1.db')
# db.set_data('Feedback', [1, 4, 4, 'хороший сервис, работают быстро, качественно, вежливо. закажу снова'])
# ______________________________________________________________________________________________________________________
# ______________________________________________________________________________________________________________________
# ______________________________________________________________________________________________________________________
# ______________________________________________________________________________________________________________________
# ______________________________________________________________________________________________________________________




# import sqlite3
#
#
# class Database:
#     def __init__(self, db_name):
#         self.__conn = sqlite3.connect(db_name)
#         self.__cur = self.__conn.cursor()
#
#     def get_column_names(self, table_name: str):
#         self.__cur.execute(f"SELECT * FROM {table_name} LIMIT 0")
#         return [description[0] for description in self.__cur.description]
#
#     def set_data(self, table_name: str, data: list):
#         self.__cur.execute(f"SELECT * FROM {table_name} LIMIT 0")
#         column_names = [description[0] for description in self.__cur.description]
#         column_names.remove('id')
#         if 'registration_date' in column_names:
#             column_names.remove('registration_date')
#         elif 'order_date' in column_names:
#             column_names.remove('order_date')
#         elif 'created_at' in column_names:
#             column_names.remove('created_at')
#         elif 'issued_at' in column_names:
#             column_names.remove('issued_at')
#
#         placeholders = ', '.join('?' for _ in range(len(data)))
#         column_names = ', '.join(column_names)
#
#         print(placeholders)
#         query = f"INSERT INTO {table_name} ({column_names}) VALUES ({placeholders})"
#         print(query)
#         print(data)
#         self.__cur.execute(query, data)
#         self.__conn.commit()
#
#     def get_data(self, table_name, row_id):
#         query = f"SELECT * FROM {table_name} WHERE id=?"
#         self.__cur.execute(query, (row_id,))
#         row = self.__cur.fetchall()[0]
#         column_names = [description[0] for description in self.__cur.description]
#         if row:
#             return row, column_names
#         else:
#             return None
#
#     def delete_data(self, table_name, row_id):
#         query = (f'''DELETE FROM
#                          {table_name}
#                      WHERE
#                          {table_name}.id = {row_id}''')
#
#         cursor = self.__cur.execute(query)
#         self.__conn.commit()
#         return cursor.fetchall()
#
#     def change_data(self, table_name: str, row_id: int, data: dict):
#         query = (f'''UPDATE {table_name}
#                      SET\n
#                  ''')
#         for key, value in data.items():
#             query += f'"{key}" = "{value}",\n'
#         query = query[:-2] + f'\nWHERE id = {row_id}'
#         print(query)
#         self.__cur.execute(query)
#         self.__conn.commit()
#
#     def own_query(self, query, data=None, fetch=True):
#         """
#         Метод для выполнения нестандартных SQL-запросов к базе данных.
#
#         :param query: SQL-запрос
#         :param data: Данные для подстановки в запрос (необязательно)
#         :param fetch: Флаг, указывающий, нужно ли извлечь данные из курсора (по умолчанию True)
#         :return: Результат выполнения запроса (если fetch=True) или None (если fetch=False)
#         """
#         if data:
#             cursor = self.__cur.execute(query, data)
#         else:
#             cursor = self.__cur.execute(query)
#
#         if fetch:
#             result = cursor.fetchall()
#             # print(result, '\n', query, '\n', data)
#             return result
#         else:
#             self.__conn.commit()
#             return None
#
#     def close(self):
#         self.__conn.close()
#
#     """
#      для записи изображения в базу данных, необходимо открыть его через
#     with с препиской rb, а затем добавить его в бд через sql-запрос
#     """
#







# ______________________________________________________________________________________________________________________
# ______________________________________________________________________________________________________________________
# ______________________________________________________________________________________________________________________
# ______________________________________________________________________________________________________________________
# ______________________________________________________________________________________________________________________














# db = Database("Database1.db")
# # db.set_data('Users', ['26546', 'Алесь', 'Борисик', 'Васильевич', '+3752451103', 'boirs@gmail.com', 'admin'])
# print(db.get_data('Users', 1))
# db.change_data('Users', 1,
#                {
#                    'telegram_id': '26546',
#                    'first_name': 'Bpzckfd',
#                    'second_name': 'Борисик',
#                    'third_name': 'Васильевич',
#                    'phone_number': '+3752451103',
#                    'email': 'boirs@gmail.com',
#                    'role': 'admin'
#                })
# print(db.get_data('Users', 1))

#
# if __name__ == "__main__":
#     pass

# def test2(x: str) -> str:
#     '''
#     питоновская функция в sql
#     :return:
#     '''
#
#     if len(x) > 10:
#         return x[:10]
#     else:
#         return x

# db.set_data('Goods', ['wef', 'rfw', 'rfwr', 'frwf', None, '123'])

# db.change_data('Goods', 4, {'name': 'варежки',
#                             'article': 'нереальные перчатки крутого гэнгсты. в них тебя будут бояться и уважать все алкаши с района',
#                             'category': 'одежда; верхняя одежда',
#                             'charasteristic': 'размер: S; цвет: чёрный панк',
#                             'picture': None,
#                             'price': '20'
#                             })

# db.set_data('Goods', ['перчатки', 'нереальные перчатки крутого гэнгсты. в них тебя будут бояться и уважать все алкаши с района', 'одежда', 'размер: S; цвет: чёрный панк', None, '20'])

# print(db.filter_goods())

# db.delete_data('Goods', 2)

#
# print(db.get_column_names('Goods'))
# db.set_data(table_name='Goods', data=['шляпа', 'головной убор крестьянина, которому позавидует любой барин',
#                                       'головные уборы; одежда', 'размер: L; цвет: светлый; матриал: солома', None,
#                                       '15'])

# print(db.get_data('Goods', 1))
# print(db.get_column_names('Goods'))

# print(db.table_filling("Receipt"))
# print(db.operations())
# db.test()

# print(db.table_filling('Goods'))
# print(db.table_filling('Warehouses'))
# print(db.table_filling('Orders'))
# print(db.table_filling('Clients'))

# with open(r'C:\Users\Алесь\PycharmProjects\PROJECT_1\goodsImages\1645328776175687133.jpg', 'rb') as photo:
#     photo = photo.read()
#     db.own_query(query=f'''
#         INSERT INTO Goods (name, article, category, charasteristic, picture, price) VALUES (?, ?, ?, ?, ?, ?)
#     ''', data=['дубинка "the rock"',
#                'Дубинка угабуги, распечатанная на 3Д принтере. Грозное оружие в походе даже на самого'
#                ' крупного мамонта. Всем угабугам рекомендовано к покупке!',
#                'toys for ugabuga',
#                'размер: XXXXL; цвет: серый; постобработка: о мамонта само сотрётся; ограничения: отсутствуют',
#                photo,
#                '300'], fetch=False)
#
# print(db.get_data('Goods', 0))

# from PyQt5 import QtCore, QtGui, QtWidgets
# import sqlite3 as sl
#
# con = sl.connect('Database1.accdb')
#
#
# class Database:
#     def __init__(self, db_name):
#         self.conn = sl.connect(db_name)
#         self.cur = self.conn.cursor()
#         self.cur.execute("CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY, value TEXT)")
#         self.conn.commit()
#
#     def get_data(self, row_id):
#         self.cur.execute("SELECT * FROM data WHERE id=?", (row_id,))
#         row = self.cur.fetchone()
#         if row:
#             return row[1]
#         else:
#             return None
#
#     def set_data(self, id, value):
#         self.cur.execute("INSERT OR REPLACE INTO data (id, value) VALUES (?, ?)", (id, value))
#         self.conn.commit()
#
#     def data_loading(self, table_name):
#
#
#         return None


# with open(r'C:\Users\Алесь\PycharmProjects\PROJECT_1\goodsImages\1645328776175687133.jpg', 'rb') as photo:
#     photo = photo.read()
#     db.own_query(query=f'''
#         INSERT INTO Goods (name, article, category, charasteristic, picture, price) VALUES (?, ?, ?, ?, ?, ?)
#     ''', data=['dildo "the rock"',
#                'Огромный член, распечатанный на 3Д принтере. Порвёт даже самую бывалую шкуру. всем рекомендовано к покупке!',
#                'toys for adult',
#                'размер: XXXXL; цвет: серый; постобработка: об дырку само слижется; ограничения: 21+',
#                photo,
#                'бесценен'])
# print(db.get_data('Goods', 0))


# шлак

# class Filter(Database):
#     def __init__(self, params, db_name):
#         super().__init__(db_name)
#         self.filter_params = params
