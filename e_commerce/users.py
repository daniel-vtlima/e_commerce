import sqlite3
from uuid import uuid4
from datetime import datetime
from e_commerce.db import get_db_connection
from e_commerce.utils import hash_password
from loguru import logger

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
        self.id = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid4())

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
            logger.success("User successfully registered!")

            return True
        except sqlite3.IntegrityError:
            logger.warning("Username already exists!")

            return False
        except sqlite3.Error as e:
            logger.error(f"An error occurred while registering the user: {e}")

            return False
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
                logger.success("Password changed successfully!")
                return True
            except sqlite3.Error as e:
                logger.error(f"An error occurred while changing the password: {e}")
            finally:
                if conn:
                    conn.close()
        else:
            logger.error("Old password is incorrect!")
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
            logger.success("User logged successfully!")
        except sqlite3.Error as e:
            logger.error(f"An error occurred during login: {e}")
            return None
        finally:
            if conn:
                conn.close()

        if user:
            return User(username, password, user[3])
        else:
            logger.error("Invalid credentials!")
            return None
