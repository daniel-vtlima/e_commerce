"""
This module provides database initialization and connection functions for an e-commerce system. 

Functions:
----------
- init_db():
    Establishes a connection to the SQLite database 'ecommerce.db'. It creates four tables if they 
    do not exist: 'users', 'products', 'carts', and 'orders'. The 'users' table stores user 
    information including username, password, and admin status. The 'products' table holds details 
    about products such as name, description, and price. The 'carts' table tracks the items in 
    users' shopping carts, and the 'orders' table stores order information.

- get_db_connection():
    Returns a connection object to the 'ecommerce.db' database, allowing further operations on the 
    database.
"""
import sqlite3

def init_db():
    """
    Establishes and returns a database connection.
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

def get_db_connection():
    """
    Initializes the database and creates necessary tables.
    """
    return sqlite3.connect("ecommerce.db")
