"""
This is the main module for an e-commerce application, providing functionality for user 
registration, login, product management, cart handling, and order placement.

The application connects to a SQLite database and includes the following functionalities:

Modules Imported:
-----------------
- `ecommerce.db`: Handles the database initialization and connection setup.
    - `init_db()`: Initializes the database and creates necessary tables.
    - `get_db_connection()`: Provides a connection to the SQLite database.
  
- `ecommerce.users`: Manages user registration, login, and user-related operations.
    - `User`: Represents a user in the system, enabling registration and login.
  
- `ecommerce.products`: Provides product management functionality for adding, editing, 
  and removing products.
    - `ProductManagement`: Handles database operations related to products.
  
- `ecommerce.cart`: Manages user carts, adding products, viewing cart contents, and 
  placing orders.
    - `Cart`: Represents a user's shopping cart and manages the items added, removed, 
      and ordered.

Functions:
----------
- `main()`: The main entry point of the application, which initializes the database and 
  performs the following actions:
    - Registers a new user.
    - Logs in the user and verifies admin access.
    - Adds a new product to the database (if the user is an admin).
    - Displays the available products.
    - Allows the user to add products to their cart.
    - Displays the cart contents.
    - Places an order based on the cart's contents.

Usage:
------
The script is executed directly to run the main function:
    `python main.py`

Example Workflow:
-----------------
1. The database is initialized.
2. A new user is registered.
3. The user logs in and, if they are an admin, can add a new product.
4. The user views the available products and adds items to their cart.
5. The user places an order, which is processed and the cart is cleared.
"""
import sqlite3
from e_commerce.db import init_db, get_db_connection
from e_commerce.users import User
from e_commerce.products import ProductManagement
from e_commerce.cart import Cart
from loguru import logger

def main():
    # Initialize the database
    init_db()

    # Establish database connection
    connection = get_db_connection()

    # User Registration
    user = User("daniel lima", "password123", True)
    user.register()

    # User Login
    logged_in_user = User.login("daniel lima", "password123")
    if logged_in_user:
        logger.success(f"User {logged_in_user.username} logged in successfully.")

        # Add Product (Admin Only)
        if logged_in_user.is_admin:
            product_repo = ProductManagement(connection)
            product_repo.add_product("Laptop", "Gaming Laptop", 1500.0)
            logger.info("Product added: Laptop")

        # View Products
        product_repo = ProductManagement(connection)
        products = product_repo.view_products()
        logger.info("Available products:")
        for product in products:
            logger.info(product)

        # Add to Cart
        cart = Cart(user_id=logged_in_user.id, connection=connection)
        cart.add_to_cart(product_id=1, quantity=2)
        logger.success("Added product to cart.")

        # View Cart
        cart_items = cart.view_cart()
        logger.info("Cart contents:")
        logger.info(cart_items)

        # Place Order
        cart.place_order()
        logger.success("Order placed successfully.")

    # Close the connection
    connection.close()

if __name__ == "__main__":
    main()
