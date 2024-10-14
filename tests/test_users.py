"""
This module contains unit tests for the User class in the e-commerce system.

Tests focus on user registration and login functionalities, utilizing pytest fixtures and mocking 
techniques to isolate the database operations.

Fixtures:
---------
- mock_hash_password: Mocks the hash_password function to return a fixed 'hashed_password' value.
- mock_db_connection: Mocks the database connection and cursor to simulate database interactions.

Test Functions:
---------------
- test_user_registration_success: Tests successful user registration and ensures database insertion.
- test_user_registration_username_exists: Tests user registration when username already exists and 
  raises an IntegrityError.
- test_user_login_success: Tests successful user login with correct credentials and fetches user data 
  from the database.
- test_user_login_invalid_credentials: Tests failed user login with incorrect credentials, returning 
  None when the user is not found.
"""

import pytest
from unittest.mock import patch, MagicMock
import sqlite3
from e_commerce.users import User
from e_commerce.db import init_db

# Fixture to mock hash_password
@pytest.fixture
def mock_hash_password():
    with patch('e_commerce.users.hash_password', return_value='hashed_password'):
        yield

# Fixture to mock database connection
@pytest.fixture
def mock_db_connection():
    with patch('e_commerce.users.get_db_connection') as mock_get_conn:
        mock_conn = MagicMock()
        mock_cursor = MagicMock()
        mock_get_conn.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        mock_conn.__enter__.return_value = mock_conn
        mock_conn.__exit__.return_value = None
        yield mock_conn, mock_cursor

def test_user_registration_success(mock_hash_password, mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection

    # Simulate successful insertion into the database
    mock_cursor.execute.return_value = None
    mock_conn.commit.return_value = None

    # Initialize the database
    init_db()

    # User Registration
    user = User("john_doe", "password123")
    result = user.register()

    # Assert that registration was successful
    assert result is True

    # Assert that the INSERT query was called
    mock_cursor.execute.assert_called_with(
        "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
        ("john_doe", "hashed_password", False)
    )
    mock_conn.commit.assert_called()

def test_user_registration_username_exists(mock_hash_password, mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection

    # Simulate IntegrityError when username exists
    mock_cursor.execute.side_effect = sqlite3.IntegrityError

    # User Registration
    user = User("john_doe", "password123")
    result = user.register()

    # Assert that registration failed
    assert result is False

    # Assert that the INSERT query was called
    mock_cursor.execute.assert_called_with(
        "INSERT INTO users (username, password, is_admin) VALUES (?, ?, ?)",
        ("john_doe", "hashed_password", False)
    )
    # Assert that commit was not called
    mock_conn.commit.assert_not_called()

def test_user_login_success(mock_hash_password, mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection

    # Simulate user found in the database
    mock_cursor.fetchone.return_value = (1, 'john_doe', 'hashed_password', False)

    # User Login
    logged_in_user = User.login("john_doe", "password123")

    # Assert that the SELECT query was called
    mock_cursor.execute.assert_called_with(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        ("john_doe", "hashed_password")
    )
    assert logged_in_user is not None
    assert logged_in_user.username == "john_doe"
    assert logged_in_user.is_admin is False

def test_user_login_invalid_credentials(mock_hash_password, mock_db_connection):
    mock_conn, mock_cursor = mock_db_connection

    # Simulate user not found in the database
    mock_cursor.fetchone.return_value = None

    # User Login
    logged_in_user = User.login("john_doe", "wrongpassword")

    # Assert that the SELECT query was called
    mock_cursor.execute.assert_called_with(
        "SELECT * FROM users WHERE username = ? AND password = ?",
        ("john_doe", "hashed_password")
    )
    assert logged_in_user is None
