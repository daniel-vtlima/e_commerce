
# E-Commerce Backend System

## Overview

This project implements a backend system for an e-commerce platform, providing functionalities such as user registration, product management, and shopping cart operations. The system is built using Python and includes SQLite for data persistence, along with unit tests to verify the correct functionality of each module.

## Project Structure

The project is organized as follows:

```
AMDEV [WSL: UBUNTU]
|
|-- __pycache__/            # Compiled bytecode cache for Python modules
|-- .gitignore              # Git ignore file to exclude unnecessary files
|-- e_commerce_tests.py     # Unit tests for the e-commerce backend system
|-- e_commerce.py           # Main backend implementation of the e-commerce system
|-- ecommerce.db            # SQLite database file used to store data
|-- poetry.lock             # Poetry lock file for dependency management
|-- pyproject.toml          # Poetry configuration file for project dependencies
|-- README.md               # Documentation about the project
|-- utils.py                # Utility functions, including database connection and password hashing
```

## Features

1. **User Management**
   - Users can register and log in to the platform.
   - Passwords are securely hashed before storage.
   - Admin users have additional privileges for product management.

2. **Product Management**
   - Admin users can add, edit, or remove products from the catalog.
   - Products have attributes such as name, description, and price.

3. **Shopping Cart Management**
   - Users can add products to their shopping cart.
   - Users can view their cart and place orders.

4. **Data Persistence**
   - All data is persisted in an SQLite database (`ecommerce.db`).

## Installation

To set up the project, follow these steps:

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd e-commerce-backend
   ```

2. **Install dependencies**
   This project uses [Poetry](https://python-poetry.org/) for dependency management. To install Poetry, refer to the [official documentation](https://python-poetry.org/docs/#installation).

   Once Poetry is installed, run:
   ```bash
   poetry install
   ```

3. **Initialize the database**
   Run the following command to initialize the SQLite database:
   ```bash
   python -c "from utils import init_db; init_db()"
   ```

## Usage

- **Run the Backend**
  The backend implementation is contained in `e_commerce.py`, which includes classes such as `User`, `ProductRepository`, and `Cart` to perform various operations.

- **Run Unit Tests**
  The unit tests are in `e_commerce_tests.py`. To run the tests:
  ```bash
  python -m unittest e_commerce_tests.py
  ```
  These tests cover user management, product management, and cart functionalities.

## Modules

### `e_commerce.py`
The main module implementing the e-commerce backend. It provides the following classes:
- `User`: Handles user registration, login, and password management.
- `ProductRepository`: Manages adding, editing, and removing products from the catalog.
- `Cart`: Manages a user's shopping cart, allowing them to add items, view the cart, and place orders.

### `e_commerce_tests.py`
This module contains unit tests for the `User`, `ProductRepository`, and `Cart` classes. It uses the `unittest` framework along with `unittest.mock` for mocking database connections and ensuring proper test isolation.

### `utils.py`
Contains utility functions, including:
- `get_db_connection()`: Establishes a connection to the SQLite database.
- `hash_password(password)`: Hashes a given password for secure storage.
- `init_db()`: Initializes the database and creates necessary tables.

## Dependencies

The main dependencies for this project include:
- **SQLite**: Used for data persistence.
- **Poetry**: For dependency management and packaging.

All dependencies are listed in `pyproject.toml`. To install them, run `poetry install` as described above.

## Contributing

If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Commit your changes (`git commit -m 'Add some feature'`).
4. Push to the branch (`git push origin feature/your-feature-name`).
5. Create a Pull Request.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Contact

If you have any questions, feel free to contact the project maintainer.
