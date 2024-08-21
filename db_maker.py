import sqlite3 as sl

# Подключение к базе данных
con = sl.connect('Database1.db')

with con:
    con.execute("""
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            telegram_id INTEGER NOT NULL,
            first_name TEXT NOT NULL,
            second_name TEXT NOT NULL,
            third_name TEXT NOT NULL,
            phone_number VARCHAR(20) NOT NULL,
            email VARCHAR(100) NOT NULL,
            role TEXT NOT NULL CHECK(role IN ('client', 'employee', 'admin')),
            registration_date DATETIME DEFAULT CURRENT_TIMESTAMP
        );
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS Orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            employee_id INTEGER,
            order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            price TEXT NOT NULL,
            discount TEXT,
            adress TEXT NOT NULL,
            status TEXT NOT NULL,
            rooms INTEGER NOT NULL,
            bathrooms INTEGER NOT NULL,
            cleaning_date DATETIME NOT NULL,
            cleaning_time TEXT NOT NULL,
            refrigerator BOOLEAN NOT NULL,
            oven BOOLEAN NOT NULL,
            boxes BOOLEAN NOT NULL,
            dishes BOOLEAN NOT NULL,
            microwave BOOLEAN NOT NULL,
            linen INTEGER NOT NULL,
            windows INTEGER NOT NULL,
            balcony INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users(id),
            FOREIGN KEY (employee_id) REFERENCES Employees(id)
        );
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS Equipment (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity >= 0),
            is_consumable BOOLEAN NOT NULL
        );
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS Feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            order_id INTEGER NOT NULL,
            rating INTEGER CHECK(rating >= 1 AND rating <= 5),
            comment TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES Users(id),            
            FOREIGN KEY (order_id) REFERENCES Orders(id)
        );
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS Employees (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            hours_per_day INTEGER NOT NULL CHECK(hours_per_day >= 0),
            hours_per_week INTEGER NOT NULL CHECK(hours_per_week >= 0),
            week INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users(id)
        );
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS EmployeesSchedule (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            date DATETIME NOT NULL,
            start_time TIME NOT NULL,
            end_time TIME NOT NULL,
            FOREIGN KEY (employee_id) REFERENCES Employees(id)
        );
    """)

    con.execute("""
        CREATE TABLE IF NOT EXISTS EquipmentIssuance (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id INTEGER NOT NULL,
            equipment_id INTEGER NOT NULL,
            order_id INTEGER NOT NULL,
            issued_quantity INTEGER NOT NULL CHECK(issued_quantity >= 0),
            return_status TEXT NOT NULL CHECK(return_status IN ('returned', 'not_returned', 'consumable')),
            issued_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            returned_at DATETIME,
            FOREIGN KEY (employee_id) REFERENCES Employees(id),
            FOREIGN KEY (equipment_id) REFERENCES Equipment(id),
            FOREIGN KEY (order_id) REFERENCES Orders(id)
        );
    """)

# Закрытие соединения с базой данных
con.close()











# import sqlite3 as sl
#
# con = sl.connect('Database1.db')
#
# with con:
#     con.execute("""
#         CREATE TABLE IF NOT EXISTS Clients (
#             id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#             first_name VARCHAR(100) NOT NULL,
#             second_name VARCHAR(100) NOT NULL,
#             lest_name VARCHAR(100) NOT NULL,
#             phone_number VARCHAR(20) NOT NULL,
#             email VARCHAR(100) NOT NULL,
#             orders_amount INTEGER NOT NULL CHECK(orders_amount >= 0)
#
#             article VARCHAR(50) NOT NULL,
#             category VARCHAR(200) NOT NULL,
#             charasteristic VARCHAR(500),
#             picture VARCHAR(250),
#         );
#     """)
#
#     con.execute("""
#         CREATE TABLE IF NOT EXISTS Warehouses (
#             id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#             adress VARCHAR(150) NOT NULL,
#             name VARCHAR(80) NOT NULL,
#             geolocation VARCHAR(150) NOT NULL
#          );
#     """)
#
#     con.execute("""
#         CREATE TABLE IF NOT EXISTS Clients (
#             id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#             name VARCHAR(200) NOT NULL,
#             contact VARCHAR(200) NOT NULL,
#             comment VARCHAR(300)
#         );
#     """)
#
#     con.execute("""
#             CREATE TABLE IF NOT EXISTS Orders (
#                 id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#                 client_id INTEGER NOT NULL,
#                 order_date VARCHAR(100) NOT NULL,
#                 status VARCHAR(80) NOT NULL,
#                 price VARCHAR(100) NOT NULL,
#                 comment VARCHAR(500),
#                 FOREIGN KEY (client_id) REFERENCES Clients (id)
#             );
#         """)
#
#     con.execute("""
#                 CREATE TABLE IF NOT EXISTS Order_content (
#                     id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#                     order_id INTEGER NOT NULL,
#                     goods_id VARCHAR(500) NOT NULL,
#                     count INTEGER NOT NULL,
#                     sum_price VARCHAR(200) NOT NULL,
#                     delivery_date VARCHAR(100) NOT NULL,
#                     expiration_date VARCHAR(100) NOT NULL,
#                     FOREIGN KEY (order_id) REFERENCES Orders (id),
#                     FOREIGN KEY (goods_id) REFERENCES Goods (id)
#                 );
#             """)
#
#     con.execute("""
#                 CREATE TABLE IF NOT EXISTS Accounting (
#                     id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#                     good_id INTEGER NOT NULL,
#                     warehouse_id INTEGER NOT NULL,
#                     count INTEGER NOT NULL,
#                     delivery_date VARCHAR(100) NOT NULL,
#                     expiration_date VARCHAR(100) NOT NULL,
#                     FOREIGN KEY (good_id) REFERENCES Goods (id),
#                     FOREIGN KEY (warehouse_id) REFERENCES Warehouses (id)
#                 );
#             """)
#
#     con.execute("""
#                 CREATE TABLE IF NOT EXISTS Write_off (
#                     id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#                     good_id INTEGER NOT NULL,
#                     warehouse_id INTEGER NOT NULL,
#                     date VARCHAR(100) NOT NULL,
#                     count INTEGER NOT NULL,
#                     reason VARCHAR(500) NOT NULL,
#                     FOREIGN KEY (good_id) REFERENCES Goods (id),
#                     FOREIGN KEY (warehouse_id) REFERENCES Warehouses (id)
#                 );
#             """)
#
#     con.execute("""
#                 CREATE TABLE IF NOT EXISTS Receipt (
#                     id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#                     good_id INTEGER NOT NULL,
#                     warehouse_id INTEGER NOT NULL,
#                     date VARCHAR(100) NOT NULL,
#                     count INTEGER NOT NULL,
#                     comment VARCHAR(500),
#                     FOREIGN KEY (good_id) REFERENCES Goods (id),
#                     FOREIGN KEY (warehouse_id) REFERENCES Warehouses (id)
#                 );
#             """)
#
#     con.execute("""
#                 CREATE TABLE IF NOT EXISTS Sale (
#                     id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#                     good_id INTEGER NOT NULL,
#                     warehouse_id INTEGER NOT NULL,
#                     client_id INTEGER NOT NULL,
#                     date VARCHAR(100) NOT NULL,
#                     count INTEGER NOT NULL,
#                     price VARCHAR(100) NOT NULL,
#                     FOREIGN KEY (good_id) REFERENCES Goods (id),
#                     FOREIGN KEY (warehouse_id) REFERENCES Warehouses (id),
#                     FOREIGN KEY (client_id) REFERENCES Clients (id)
#                 );
#             """)
#
#     con.execute("""
#                 CREATE TABLE IF NOT EXISTS Transfer (
#                     id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#                     good_id INTEGER NOT NULL,
#                     from_warehouse_id INTEGER NOT NULL,
#                     to_warehouse_id INTEGER NOT NULL,
#                     date VARCHAR(100) NOT NULL,
#                     count INTEGER NOT NULL,
#                     comment VARCHAR(500),
#                     FOREIGN KEY (good_id) REFERENCES Goods (id)
#                 );
#             """)
#
#
#
