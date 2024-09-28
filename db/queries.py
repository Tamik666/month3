CREATE_TABLE_PRODUCTS = """
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        name_product VARCHAR(255),
        category VARCHAR(255),
        size VARCHAR(255),
        price VARCHAR(255),
        art VARCHAR(255),
        quantity VARCHAR(255),
        photo TEXT
    )
"""
INSERT_PRODUCTS_QUERY = """
    INSERT INTO products (name_product, category, size, price, art, quantity, photo)
    VALUES (?, ?, ?, ?, ?, ?, ?)
"""