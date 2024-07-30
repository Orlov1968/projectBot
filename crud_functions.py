import sqlite3

connection = sqlite3.connect("sql_products.db")
cursor = connection.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS Products(
     id INTEGER PRIMARY KEY,
     title TEXT NOT NULL,
     description TEXT,
     price INTEGER NOT NULL
     )
     ''')
cursor.execute("CREATE INDEX IF NOT EXISTS idx_price ON Products (price)")

list_of_products = [
    ("мочегон", "бегать в туалет часто", 90),
    ("жиросжёг", "потеть постоянно", 560),
    ("блевотин", "извергать еду", 240),
    ("поносин", "так же в туалет", 130)
]
cursor.executemany("INSERT INTO Products (title, description, price) VALUES (?, ?, ?)", list_of_products)

# cursor.execute("SELECT * FROM Products")
# products = cursor.fetchall()

connection.commit()
# connection.close()


def get_of_products():
    cursor.execute("SELECT * FROM Products")
    products = cursor.fetchall()
    return products
