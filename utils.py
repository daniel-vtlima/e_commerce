"""
Docstring
"""
import sqlite3
import hashlib


def init_db():
    """
    Doc
    """
    conn = sqlite3.connect("ecommerce.db")
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    is_admin BOOLEAN NOT NULL
                )""")
    c.execute("""CREATE TABLE IF NOT EXISTS products (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    description TEXT,
                    price REAL NOT NULL
                )""")
    c.execute("""CREATE TABLE IF NOT EXISTS carts (
                    user_id INTEGER,
                    product_id INTEGER,
                    quantity INTEGER,
                    PRIMARY KEY (user_id, product_id)
                )""")
    c.execute("""CREATE TABLE IF NOT EXISTS orders (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    product_details TEXT NOT NULL
                )""")
    conn.commit()
    conn.close()

def hash_password(password: str) -> str:
    """
    Hashes the password using SHA-256.
    
    :param password: The plain text password to be hashed.
    :return: The hashed password as a hexadecimal string.
    """
    return hashlib.sha256(password.encode()).hexdigest()

def get_db_connection():
    """
    Doc
    """
    return sqlite3.connect("ecommerce.db")
