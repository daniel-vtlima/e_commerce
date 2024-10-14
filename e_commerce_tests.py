"""
This module contains unit tests for the main functionalities of the e-commerce backend system.

The tests include:
    - User registration, login, and password management.
    - Product management (adding products to the catalog).
    - Shopping cart functionality (adding items, placing orders).

The module uses the unittest framework along with unittest.mock for mocking database connections and interactions.
"""
import unittest
from unittest.mock import patch, MagicMock
from e_commerce import User, ProductManagement, Cart
from utils import init_db

class TestMainFunction(unittest.TestCase):
    @patch('e_commerce.get_db_connection')
    def test_main_function(self, mock_get_db_connection):
        # Mock the database connection and cursor
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_db_connection.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.__enter__.return_value = mock_conn
        mock_conn.__exit__.return_value = None

        # Mocking hash_password in the 'e_commerce' module
        with patch('e_commerce.hash_password', return_value='hashed_password'):
            # Initialize the database
            init_db()
            
            # User Registration
            user = User("daniel lima", "password123")
            user.register()
            
            # Check if user registration inserts into the database
            mock_cursor.execute.assert_any_call(
                "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
                ("daniel lima", "hashed_password", False)
            )
            # Commit the transaction for user registration
            mock_conn.commit.assert_called()

            # User Login
            # Set fetchone to return the user data during login
            mock_cursor.fetchone.return_value = (1, 'daniel lima', 'hashed_password', False)
            logged_in_user = User.login("daniel lima", "password123")
            self.assertIsNotNone(logged_in_user)
            self.assertEqual(logged_in_user.username, "daniel lima")

            # Create a ProductManagement instance
            product_repo = ProductManagement(mock_conn)

            # Add Product (Admin Only)
            logged_in_user.is_admin = True  # Set user as admin to allow adding products
            product_repo.add_product("Laptop", "Gaming Laptop", 1500.0)

            # Check if add_product inserts into the database
            mock_cursor.execute.assert_any_call(
                "INSERT INTO products (name, description, price) VALUES (?, ?, ?)",
                ("Laptop", "Gaming Laptop", 1500.0)
            )

            # Add to Cart
            cart = Cart(user_id=1, connection=mock_conn)
            cart.add_to_cart(product_id=1, quantity=2)

            # Check if add_to_cart inserts or replaces into the database
            mock_cursor.execute.assert_any_call(
                "INSERT OR REPLACE INTO carts (user_id, product_id, quantity) VALUES (?, ?, ?)",
                (1, 1, 2)
            )

            # Place Order
            # Set fetchall to return cart items
            mock_cursor.fetchall.return_value = [(1, 2)]  # Mock cart items
            cart.place_order()

            # Check if place_order inserts into orders and clears the cart
            mock_cursor.execute.assert_any_call(
                "INSERT INTO orders (user_id, product_details) VALUES (?, ?)",
                (1, "Product ID: 1, Quantity: 2")
            )
            mock_cursor.execute.assert_any_call(
                "DELETE FROM carts WHERE user_id = ?",
                (1,)
            )

if __name__ == "__main__":
    unittest.main()
    