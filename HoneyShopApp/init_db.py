import sqlite3

connection = sqlite3.connect('database.db')

cursor = connection.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        price INTEGER NOT NULL,
        description TEXT,
        image TEXT,
        category TEXT NOT NULL
    )
''')

cursor.execute(
    "INSERT INTO products (name, price, description, image, category) VALUES (?, ?, ?, ?, ?)",
    ('Miere de tei', 35, '1 kg', 'honey_jar.jpg', 'honey')
)

cursor.execute(
    "INSERT INTO products (name, price, description, image, category) VALUES (?, ?, ?, ?, ?)",
    ('Albine', 15, 'mica', 'wax_bear.jpg', 'wax')
)
connection.commit()
connection.close()

print("Database built successfully!")


