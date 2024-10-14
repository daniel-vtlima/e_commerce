"""
This module provides a class representing a user's shopping cart in an e-commerce system.

Classes:
--------
- Cart:
    Represents a shopping cart for a user, allowing products to be added, viewed, and ordered.

    Attributes:
    -----------
    - user_id (int): The ID of the user.
    - connection: A database connection object for performing operations.

    Methods:
    --------
    - __init__(user_id: int, connection):
        Initializes the Cart with a specific user ID and a database connection.

    - add_to_cart(product_id: int, quantity: int) -> None:
        Adds a specified quantity of a product to the user's cart in the database.

    - view_cart() -> list[dict]:
        Retrieves the contents of the user's cart from the database. Returns a list of dictionaries
        where each dictionary contains a product ID and the corresponding quantity.

    - place_order() -> None:
        Places an order for all items currently in the user's cart. The cart is cleared after the 
        order is placed, and an entry is added to the 'orders' table in the database.
"""
from e_commerce.db import get_db_connection

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
