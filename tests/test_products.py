"""
This module contains unit tests for the ProductManagement class in the e-commerce system.

Tests focus on product-related operations such as adding, editing, removing, and viewing products.
The tests use pytest and mocking to isolate the database operations and ensure accurate behavior.

Fixtures:
---------
- mock_db_connection: Mocks the database connection and cursor to simulate SQL operations.

Test Functions:
---------------
- test_add_product: Tests that a product is correctly added to the database.
- test_add_product_exception: Tests that a RuntimeError is raised when product addition fails.
- test_edit_product: Tests that a product is correctly edited in the database.
- test_edit_product_exception: Tests that a RuntimeError is raised when product editing fails.
- test_remove_product: Tests that a product is correctly removed from the database.
- test_remove_product_exception: Tests that a RuntimeError is raised when product removal fails.
- test_view_products: Tests that products are correctly retrieved from the database.
- test_view_products_exception: Tests that a RuntimeError is raised when product retrieval fails.
"""

import pytest
from unittest.mock import MagicMock, patch
from e_commerce.products import ProductManagement

@pytest.fixture
def mock_db_connection():
    with patch('e_commerce.products.get_db_connection') as mock_get_conn:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        # Support for 'with' statements
        mock_conn.__enter__.return_value = mock_conn
        mock_conn.__exit__.return_value = None
        yield mock_conn, mock_cursor

def test_add_product(mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection
    product_repo = ProductManagement(connection=mock_conn)

    # Call the method under test
    product_repo.add_product(name='Laptop', description='Gaming Laptop', price=1500.0)

    # Assert that the correct SQL query was executed with expected parameters
    mock_cursor.execute.assert_called_with(
        "INSERT INTO products (name, description, price) VALUES (?, ?, ?)",
        ('Laptop', 'Gaming Laptop', 1500.0)
    )

def test_add_product_exception(mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection
    product_repo = ProductManagement(connection=mock_conn)

    # Simulate an exception during database operation
    mock_cursor.execute.side_effect = Exception('Database Error')

    # Assert that RuntimeError is raised with correct message
    with pytest.raises(RuntimeError) as exc_info:
        product_repo.add_product(name='Laptop', description='Gaming Laptop', price=1500.0)

    assert 'Failed to add product: Database Error' in str(exc_info.value)

def test_edit_product(mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection
    product_repo = ProductManagement(connection=mock_conn)

    # Call the method under test
    product_repo.edit_product(product_id=1, name='Ultrabook', description='Lightweight Laptop', price=2000.0)

    # Assert that the correct SQL query was executed with expected parameters
    mock_cursor.execute.assert_called_with(
        "UPDATE products SET name = ?, description = ?, price = ? WHERE id = ?",
        ('Ultrabook', 'Lightweight Laptop', 2000.0, 1)
    )

def test_edit_product_exception(mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection
    product_repo = ProductManagement(connection=mock_conn)

    # Simulate an exception
    mock_cursor.execute.side_effect = Exception('Database Error')

    # Assert that RuntimeError is raised
    with pytest.raises(RuntimeError) as exc_info:
        product_repo.edit_product(product_id=1, name='Ultrabook', description='Lightweight Laptop', price=2000.0)

    assert 'Failed to edit product: Database Error' in str(exc_info.value)

def test_remove_product(mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection
    product_repo = ProductManagement(connection=mock_conn)

    # Call the method under test
    product_repo.remove_product(product_id=1)

    # Assert that the correct SQL query was executed with expected parameters
    mock_cursor.execute.assert_called_with(
        "DELETE FROM products WHERE id = ?", (1,)
    )

def test_remove_product_exception(mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection
    product_repo = ProductManagement(connection=mock_conn)

    # Simulate an exception
    mock_cursor.execute.side_effect = Exception('Database Error')

    # Assert that RuntimeError is raised
    with pytest.raises(RuntimeError) as exc_info:
        product_repo.remove_product(product_id=1)

    assert 'Failed to remove product: Database Error' in str(exc_info.value)

def test_view_products(mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection
    product_repo = ProductManagement(connection=mock_conn)

    # Mock the data returned by fetchall
    mock_cursor.fetchall.return_value = [
        (1, 'Laptop', 'Gaming Laptop', 1500.0),
        (2, 'Smartphone', 'Latest Model', 800.0)
    ]

    # Call the method under test
    products = product_repo.view_products()

    # Assert that the correct SQL query was executed
    mock_cursor.execute.assert_called_with(
        "SELECT id, name, description, price FROM products"
    )

    # Assert that the method returns the expected data
    expected_products = [
        {'id': 1, 'name': 'Laptop', 'description': 'Gaming Laptop', 'price': 1500.0},
        {'id': 2, 'name': 'Smartphone', 'description': 'Latest Model', 'price': 800.0}
    ]
    assert products == expected_products

def test_view_products_exception(mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection
    product_repo = ProductManagement(connection=mock_conn)

    # Simulate an exception
    mock_cursor.execute.side_effect = Exception('Database Error')

    # Assert that RuntimeError is raised
    with pytest.raises(RuntimeError) as exc_info:
        product_repo.view_products()

    assert 'Failed to view products: Database Error' in str(exc_info.value)
