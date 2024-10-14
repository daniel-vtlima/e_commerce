"""
This module contains unit tests for the e-commerce backend system, which includes user 
registration, product management, and cart functionalities.

Classes:
    TestUser: Contains unit tests for the User class, including user registration, password change,
              and login functionality.
    TestProductManagement: Contains unit tests for the ProductRepository class, which manages
                           adding, editing, and removing products.
    TestCart: Contains unit tests for the Cart class, including adding items to the cart, viewing
              the cart, and placing orders.

Usage:
    Run this module to execute all unit tests for the e-commerce backend system.
"""
import unittest
from unittest.mock import patch, MagicMock
from utils import get_db_connection, hash_password, init_db
from main import User, ProductRepository, Cart

class TestUser(unittest.TestCase):
    @patch('utils.get_db_connection')
    def test_register_user(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        user = User("test_user", "password123")
        user.register()
        mock_conn.cursor().execute.assert_called_with(
            "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
            ("test_user", hash_password("password123"), False)
        )

    @patch('utils.get_db_connection')
    def test_change_password(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        user = User("test_user", "password123")
        user.change_password("password123", "new_password123")
        mock_conn.cursor().execute.assert_called_with(
            "UPDATE users SET password = ? WHERE username = ?",
            (hash_password("new_password123"), "test_user")
        )

    @patch('utils.get_db_connection')
    def test_login(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor().fetchone.return_value = ("test_user", hash_password("password123"), False)
        user = User.login("test_user", "password123")
        self.assertIsNotNone(user)
        self.assertEqual(user.username, "test_user")

class TestProductManagement(unittest.TestCase):
    @patch('utils.get_db_connection')
    def test_add_product(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        product_repo = ProductRepository(mock_conn)
        product_repo.add_product("Laptop", "Gaming Laptop", 1500.0)
        mock_conn.cursor().execute.assert_called_with(
            "INSERT INTO products (name, description, price) VALUES (?, ?, ?)",
            ("Laptop", "Gaming Laptop", 1500.0)
        )

    @patch('utils.get_db_connection')
    def test_edit_product(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        product_repo = ProductRepository(mock_conn)
        product_repo.edit_product(1, "Laptop", "Updated Gaming Laptop", 1400.0)
        mock_conn.cursor().execute.assert_called_with(
            "UPDATE products SET name = ?, description = ?, price = ? WHERE id = ?",
            ("Laptop", "Updated Gaming Laptop", 1400.0, 1)
        )

    @patch('utils.get_db_connection')
    def test_remove_product(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        product_repo = ProductRepository(mock_conn)
        product_repo.remove_product(1)
        mock_conn.cursor().execute.assert_called_with(
            "DELETE FROM products WHERE id = ?", (1,)
        )

class TestCart(unittest.TestCase):
    @patch('utils.get_db_connection')
    def test_add_to_cart(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        cart = Cart(user_id=1, connection=mock_conn)
        cart.add_to_cart(product_id=1, quantity=2)
        mock_conn.cursor().execute.assert_called_with(
            "INSERT OR REPLACE INTO carts (user_id, product_id, quantity) VALUES (?, ?, ?)",
            (1, 1, 2)
        )

    @patch('utils.get_db_connection')
    def test_view_cart(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor().fetchall.return_value = [(1, 2)]
        cart = Cart(user_id=1, connection=mock_conn)
        cart_items = cart.view_cart()
        self.assertEqual(len(cart_items), 1)
        self.assertEqual(cart_items[0]['product_id'], 1)
        self.assertEqual(cart_items[0]['quantity'], 2)

    @patch('utils.get_db_connection')
    def test_place_order(self, mock_get_db_connection):
        mock_conn = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor().fetchall.return_value = [(1, 2)]
        cart = Cart(user_id=1, connection=mock_conn)
        cart.place_order()
        mock_conn.cursor().execute.assert_any_call(
            "INSERT INTO orders (user_id, product_details) VALUES (?, ?)",
            (1, "Product ID: 1, Quantity: 2")
        )
        mock_conn.cursor().execute.assert_any_call(
            "DELETE FROM carts WHERE user_id = ?", (1,)
        )

if __name__ == "__main__":
    unittest.main()