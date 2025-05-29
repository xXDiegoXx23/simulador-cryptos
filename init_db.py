import sqlite3

connection = sqlite3.connect('movements.db')

with connection:
    connection.execute('''
        CREATE TABLE IF NOT EXISTS movements (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            time TEXT,
            from_currency TEXT,
            from_quantity REAL,
            to_currency TEXT,
            to_quantity REAL
        )
    ''')

print("Base de datos creada correctamente.")