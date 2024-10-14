
# E-Commerce System

This project is a basic implementation of an e-commerce system using SQLite as the database. The system includes functionality for managing users, products, carts, and orders.

## Project Structure

```
e_commerce/
│
├── cart.py          # Handles cart operations such as adding to cart and placing orders.
├── db.py            # Database initialization and connection management.
├── products.py      # Manages product-related operations such as adding and viewing products.
├── users.py         # Handles user registration, login, and authentication.
├── utils.py         # Contains utility functions (if any).
├── __init__.py      # Makes the `e_commerce` a package.
│
tests/
│
├── test_cart.py     # Unit tests for cart functionality.
├── test_products.py # Unit tests for product management functionality.
├── test_users.py    # Unit tests for user-related functionality.
├── __init__.py      # Makes the `tests` a package.
│
├── .gitignore       # File specifying which files to ignore in version control.
├── ecommerce.db     # SQLite database file storing the e-commerce data.
├── main.py          # Entry point for the application, handling user registration, login, etc.
├── README.md        # This file, describing the project.
├── pyproject.toml   # Python project configuration file for dependency management.
├── poetry.lock      # Lock file for managing exact dependencies for the project.
```

## Features

- **User Management**: Register new users, login, and handle admin privileges.
- **Product Management**: Admin users can add, update, and delete products.
- **Shopping Cart**: Users can add products to their cart, view cart contents, and place orders.
- **Order Placement**: Users can place orders based on their cart contents.

## Setup Instructions

### Prerequisites

- Python 3.9+
- [Poetry](https://python-poetry.org/docs/) for dependency management.

### Installation

1. Clone the repository.
2. Navigate to the project directory and install dependencies using Poetry:

   ```
   poetry install
   ```

3. Initialize the database by running the `main.py` file.

   ```
   python main.py
   ```

4. Run tests using pytest:

   ```
   pytest
   ```

## Running the Application

1. After setting up the database, you can execute the main application using:

   ```
   python main.py
   ```

This will allow you to register users, log in, and perform other e-commerce functionalities.

## Running Tests

Tests are included in the `tests/` directory, and you can run them with pytest as follows:

```
pytest
```

This will run unit tests for user management, product management, and cart functionalities.

## License

This project is licensed under the MIT License.
