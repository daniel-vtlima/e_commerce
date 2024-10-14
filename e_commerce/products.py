"""
This module provides a class for managing products in an e-commerce system.

Classes:
--------
- ProductManagement:
    A repository class for performing database operations related to products.

    Attributes:
    -----------
    - connection: A database connection object for performing product-related queries.

    Methods:
    --------
    - __init__(connection):
        Initializes the ProductManagement object with a provided database connection.

    - add_product(name: str, description: str, price: float) -> None:
        Adds a new product to the database with the specified name, description, and price.

    - edit_product(product_id: int, name: str, description: str, price: float) -> None:
        Updates an existing product's name, description, and price in the database using the 
        product's ID.

    - remove_product(product_id: int) -> None:
        Deletes a product from the database by its ID.

    - view_products() -> list[dict]:
        Retrieves all products from the database and returns them as a list of dictionaries, each 
        containing the product ID, name, description, and price.
"""
from e_commerce.db import get_db_connection

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
