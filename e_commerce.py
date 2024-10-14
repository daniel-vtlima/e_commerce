"""
This module implements a backend system for an e-commerce platform where users can register, log in,
manage products, add products to their cart, and place orders. It includes user authentication with
secure password storage, and data is persisted using SQLite.

Classes:
    User: Represents a user with methods for registration, login, and password management.
    ProductManagement: Manages products, providing methods to add, edit, remove, and view products.
    Cart: Manages a user's shopping cart with methods to add products, view the cart, and place orders.

Functions:
    init_db: Initializes the SQLite database and creates necessary tables.

Usage:
    - Users can register and log in to manage their account.
    - Admin users can add, edit, or remove products from the catalog.
    - Logged-in users can add products to their cart, view their cart, and place orders.

Error Handling:
    - Handles duplicate usernames during registration.
    - Handles empty cart scenarios when placing an order.
    - Prints error messages for invalid credentials during login.

Security:
    - Passwords are securely hashed before being stored in the database.
"""
import sqlite3
from utils import get_db_connection, hash_password, init_db

class User:
    """
    Represents a user in the e-commerce platform, providing methods for registration, login,
    and password management.

    Attributes:
        username (str): The username of the user.
        password (str): The hashed password of the user.
        is_admin (bool): Indicates if the user is an admin.
    """
    def __init__(self, username: str, password: str, is_admin: bool = False):
        """
        Initializes a User object.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.
            is_admin (bool, optional): Indicates if the user is an admin. Defaults to False.
        """
        self.username = username
        self.password = hash_password(password)
        self.is_admin = is_admin

    def register(self) -> None:
        """
        Registers the user by inserting their details into the database.
        """
        try:
            conn = get_db_connection()
            c = conn.cursor()
            c.execute("INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
                      (self.username, self.password, self.is_admin))
            conn.commit()
        except sqlite3.IntegrityError:
            print("Username already exists!")
        except sqlite3.Error as e:
            print(f"An error occurred while registering the user: {e}")
        finally:
            if conn:
                conn.close()

    def change_password(self, old_password: str, new_password: str) -> bool:
        """
        Changes the user's password after verifying the old password.

        Args:
            old_password (str): The current password of the user.
            new_password (str): The new password to be set.

        Returns:
            bool: True if the password was successfully changed, False otherwise.
        """
        if hash_password(old_password) == self.password:
            try:
                self.password = hash_password(new_password)
                conn = get_db_connection()
                c = conn.cursor()
                c.execute("UPDATE users SET password = ? WHERE username = ?", (self.password, self.username))
                conn.commit()
                print("Password changed successfully!")
                return True
            except sqlite3.Error as e:
                print(f"An error occurred while changing the password: {e}")
            finally:
                if conn:
                    conn.close()
        else:
            print("Old password is incorrect!")
            return False

    @staticmethod
    def login(username: str, password: str):
        """
        Logs in the user by checking their credentials.

        Args:
            username (str): The username of the user.
            password (str): The password of the user.

        Returns:
            User: User object if credentials are correct, None otherwise.
        """
        try:
            conn = get_db_connection()
            c = conn.cursor()
            hashed_pw = hash_password(password)
            c.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, hashed_pw))
            user = c.fetchone()
        except sqlite3.Error as e:
            print(f"An error occurred during login: {e}")
            return None
        finally:
            if conn:
                conn.close()

        if user:
            return User(username, password, user[3])
        else:
            print("Invalid credentials!")
            return None

class ProductManagement:
    """
    Repository class for performing database operations related to products.

    Attributes:
        connection: A database connection object.
    """
    def __init__(self, connection):
        """
        Initializes the ProductManagement with a database connection.

        Args:
            connection: A database connection object.
        """
        self.connection = connection

    def add_product(self, name: str, description: str, price: float) -> None:
        """
        Adds a new product to the database.

        Args:
            name (str): Name of the product.
            description (str): Description of the product.
            price (float): Price of the product.
        """
        try:
            with self.connection as conn:
                cursor = conn.cursor()
                cursor.execute("INSERT INTO products (name, description, price) VALUES (?, ?, ?)",
                               (name, description, price))
        except Exception as e:
            raise RuntimeError(f"Failed to add product: {e}")

    def edit_product(self, product_id: int, name: str, description: str, price: float) -> None:
        """
        Edits an existing product in the database.

        Args:
            product_id (int): ID of the product to be edited.
            name (str): New name of the product.
            description (str): New description of the product.
            price (float): New price of the product.
        """
        try:
            with self.connection as conn:
                cursor = conn.cursor()
                cursor.execute("UPDATE products SET name = ?, description = ?, price = ? WHERE id = ?",
                               (name, description, price, product_id))
        except Exception as e:
            raise RuntimeError(f"Failed to edit product: {e}")

    def remove_product(self, product_id: int) -> None:
        """
        Removes a product from the database.

        Args:
            product_id (int): ID of the product to be removed.
        """
        try:
            with self.connection as conn:
                cursor = conn.cursor()
                cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        except Exception as e:
            raise RuntimeError(f"Failed to remove product: {e}")

    def view_products(self) -> list[dict]:
        """
        Retrieves a list of all products from the database.

        Returns:
            list[dict]: A list of all products, each represented as a dictionary.
        """
        try:
            with self.connection as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT id, name, description, price FROM products")
                products = cursor.fetchall()
                return [
                    {"id": row[0], "name": row[1], "description": row[2], "price": row[3]}
                    for row in products
                ]
        except Exception as e:
            raise RuntimeError(f"Failed to view products: {e}")

class Cart:
    """
    Represents a user's shopping cart, allowing items to be added, viewed, and ordered.

    Attributes:
        user_id (int): The ID of the user.
        connection: A database connection object.
    """
    def __init__(self, user_id: int, connection):
        """
        Initializes a Cart object for a specific user.

        Args:
            user_id (int): The ID of the user.
            connection: A database connection object.
        """
        self.user_id = user_id
        self.connection = connection

    def add_to_cart(self, product_id: int, quantity: int) -> None:
        """
        Adds a product to the user's cart.

        Args:
            product_id (int): The ID of the product to add.
            quantity (int): The quantity of the product to add.
        """
        try:
            with self.connection as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT OR REPLACE INTO carts (user_id, product_id, quantity) VALUES (?, ?, ?)",
                    (self.user_id, product_id, quantity)
                )
        except Exception as e:
            raise RuntimeError(f"Failed to add product to cart: {e}")

    def view_cart(self) -> list[dict]:
        """
        Retrieves the contents of the user's cart.

        Returns:
            list[dict]: A list of dictionaries containing product IDs and their quantities in the cart.
        """
        try:
            with self.connection as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT product_id, quantity FROM carts WHERE user_id = ?", (self.user_id,))
                cart_items = cursor.fetchall()
                return [
                    {"product_id": item[0], "quantity": item[1]}
                    for item in cart_items
                ]
        except Exception as e:
            raise RuntimeError(f"Failed to view cart: {e}")

    def place_order(self) -> None:
        """
        Places an order for the items in the user's cart and clears the cart after placing the order.
        """
        try:
            with self.connection as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT product_id, quantity FROM carts WHERE user_id = ?", (self.user_id,))
                cart_items = cursor.fetchall()

                if not cart_items:
                    raise ValueError("Cart is empty! Cannot place an order.")

                product_details = ", ".join([f"Product ID: {item[0]}, Quantity: {item[1]}" for item in cart_items])
                cursor.execute("INSERT INTO orders (user_id, product_details) VALUES (?, ?)",
                               (self.user_id, product_details))
                cursor.execute("DELETE FROM carts WHERE user_id = ?", (self.user_id,))
        except ValueError as ve:
            print(ve)
        except Exception as e:
            raise RuntimeError(f"Failed to place order: {e}")
        else:
            print("Order placed successfully!")

# Initialize the database
init_db()

# Example Usage
if __name__ == "__main__":
    # User Registration
    user = User("daniel lima", "password123")
    user.register()

    # User Login
    logged_in_user = User.login("daniel lima", "password123")
    if logged_in_user:
        # Create a database connection
        conn = get_db_connection()

        # Create a ProductManagement instance
        product_repo = ProductManagement(conn)

        # Add Product (Admin Only)
        if logged_in_user.is_admin:
            product_repo.add_product("Laptop", "Gaming Laptop", 1500.0)

        # View Products
        products = product_repo.view_products()
        for product in products:
            print(product)

        # Add to Cart
        cart = Cart(user_id=1, connection=conn)
        cart.add_to_cart(product_id=1, quantity=2)

        # View Cart
        cart_items = cart.view_cart()
        print(cart_items)

        # Place Order
        cart.place_order()
        