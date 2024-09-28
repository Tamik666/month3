import sqlite3
from db import queries

store_db = sqlite3.connect("db/store.sqlite3")
store_cursor = store_db.cursor()

def sql_create_products():
    if store_db:
        print("Store database successfully connected")
    store_cursor.execute(queries.CREATE_TABLE_PRODUCTS)
    store_db.commit()

def sql_insert_products(name_product, category, size, price, art, quantity, photo):
    store_cursor.execute(queries.INSERT_PRODUCTS_QUERY, (name_product, category, size, price, art, quantity, photo))
    store_db.commit()

def check_art_exists(art):
    store_cursor.execute("SELECT * FROM products WHERE art = ?",(art,))
    return store_cursor.fetchone() is not None

def get_available_arts():
    store_cursor.execute("SELECT art FROM products")
    return [row[0] for row in store_cursor.fetchall()]

def check_size_stock(size):
    store_cursor.execute("SELECT * FROM products WHERE size = ?", (size,))
    return store_cursor.fetchone() is not None

def check_size_available(size):
    store_cursor.execute("SELECT size FROM products WHERE art = ?", (size,))
    result = store_cursor.fetchone()
    return result[0] if result else 0

def check_product_stock(art):
    store_cursor.execute("SELECT quantity FROM products WHERE art = ?", (art,))
    result = store_cursor.fetchone()
    return result[0] if result else 0
