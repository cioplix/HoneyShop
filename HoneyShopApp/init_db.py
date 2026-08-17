import sqlite3
from werkzeug.security import generate_password_hash
connection = sqlite3.connect('database.db')

cursor = connection.cursor()

# 1. Create the Products Table
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

# 2. Insert test products
cursor.execute(
    "INSERT INTO products (name, price, description, image, category) VALUES (?, ?, ?, ?, ?)",
    ('Miere de tei', 35, '1 kg', 'honey_jar.jpg', 'honey')
)

cursor.execute(
    "INSERT INTO products (name, price, description, image, category) VALUES (?, ?, ?, ?, ?)",
    ('Albine', 15, 'mica', 'wax_bear.jpg', 'wax')
)

# ---------------------------------------------------------
# 3. Create the NEW Orders Table right here!
# ---------------------------------------------------------
cursor.execute('''
    CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        customer_name TEXT NOT NULL,
        phone TEXT NOT NULL,
        delivery_method TEXT NOT NULL,
        address TEXT NOT NULL,
        order_summary TEXT NOT NULL,
        total_price REAL NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

print("Database built successfully!")

#4. Account Database

# Create the Users Table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL,
        phone TEXT,
        address TEXT,
        role TEXT DEFAULT 'customer'
    )
''')
#facem contul de admin
admin_password = generate_password_hash('ADMIN123ADMIN')
cursor.execute(
    "INSERT INTO users (name, email, password, phone, address,role) VALUES (?, ?, ?, ?, ?,?)",
    ('ADMIN', 'admin@admin.com', admin_password, '0700000000', 'ADMINHousehold','admin')
)

connection.commit()
connection.close()