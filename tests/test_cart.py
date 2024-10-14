"""
This module contains unit tests for the Cart class in the e-commerce system.

Tests focus on cart-related operations such as adding products to the cart, viewing cart contents,
and placing orders. The tests utilize pytest fixtures and mocking to simulate database interactions.

Fixtures:
---------
- mock_db_connection: Mocks the database connection and cursor for SQL operations.

Test Functions:
---------------
- test_add_to_cart: Tests that a product is correctly added to the user's cart in the database.
- test_view_cart: Tests that the contents of the user's cart are correctly retrieved from the 
  database.
- test_place_order_success: Tests that a valid order is placed successfully, cart is cleared, and 
  order is inserted into the database.
- test_place_order_empty_cart: Tests that placing an order with an empty cart results in an 
  appropriate message and no further SQL operations.
"""

import pytest
from unittest.mock import patch, MagicMock
from e_commerce.cart import Cart

# Fixture to mock database connection
@pytest.fixture
def mock_db_connection():
    with patch('e_commerce.cart.get_db_connection') as mock_get_conn:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.__enter__.return_value = mock_conn
        mock_conn.__exit__.return_value = None
        yield mock_conn, mock_cursor

def test_add_to_cart(mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection
    cart = Cart(user_id=1, connection=mock_conn)

    # Test adding to cart
    cart.add_to_cart(product_id=10, quantity=2)

    # Assert that the correct SQL query was executed
    mock_cursor.execute.assert_called_with(
        "INSERT OR REPLACE INTO carts (user_id, product_id, quantity) VALUES (?, ?, ?)",
        (1, 10, 2)
    )

def test_view_cart(mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection
    cart = Cart(user_id=1, connection=mock_conn)

    # Mock the database response
    mock_cursor.fetchall.return_value = [(10, 2), (20, 1)]

    # Call view_cart
    cart_items = cart.view_cart()

    # Assert that the correct SQL query was executed
    mock_cursor.execute.assert_called_with(
        "SELECT product_id, quantity FROM carts WHERE user_id = ?", (1,)
    )

    # Assert that the returned cart items are as expected
    expected_items = [
        {"product_id": 10, "quantity": 2},
        {"product_id": 20, "quantity": 1}
    ]
    assert cart_items == expected_items

def test_place_order_success(mock_db_connection, capsys):
    mock_conn, mock_cursor = mock_db_connection
    cart = Cart(user_id=1, connection=mock_conn)

    # Mock the database response for cart items
    mock_cursor.fetchall.return_value = [(10, 2), (20, 1)]

    # Call place_order
    cart.place_order()

    # Capture printed output
    captured = capsys.readouterr()
    assert "Order placed successfully!" in captured.out

    # Assert that SELECT was called to get cart items
    mock_cursor.execute.assert_any_call(
        "SELECT product_id, quantity FROM carts WHERE user_id = ?", (1,)
    )

    # Assert that INSERT INTO orders was called
    expected_product_details = "Product ID: 10, Quantity: 2, Product ID: 20, Quantity: 1"
    mock_cursor.execute.assert_any_call(
        "INSERT INTO orders (user_id, product_details) VALUES (?, ?)",
        (1, expected_product_details)
    )

    # Assert that DELETE FROM carts was called
    mock_cursor.execute.assert_any_call(
        "DELETE FROM carts WHERE user_id = ?", (1,)
    )

def test_place_order_empty_cart(mock_db_connection, capsys):
    mock_conn, mock_cursor = mock_db_connection
    cart = Cart(user_id=1, connection=mock_conn)

    # Mock the database response to return empty cart
    mock_cursor.fetchall.return_value = []

    # Call place_order
    cart.place_order()

    # Capture printed output
    captured = capsys.readouterr()
    assert "Cart is empty! Cannot place an order." in captured.out

    # Assert that SELECT was called to get cart items
    mock_cursor.execute.assert_called_with(
        "SELECT product_id, quantity FROM carts WHERE user_id = ?", (1,)
    )

    # Assert that no further SQL queries were executed
    assert mock_cursor.execute.call_count == 1
