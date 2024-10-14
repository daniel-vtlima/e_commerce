# E-commerce Backend System

This repository contains the backend code for a simple e-commerce platform, designed to provide functionalities such as user registration, login, product management, shopping cart operations, and order placements. It is built using Python and SQLite to handle data persistence.

## Features

- **User Management**: Users can register, log in, and change their passwords. Admins have additional privileges to manage products.
- **Product Management**: Admin users can add, edit, or remove products from the catalog.
- **Shopping Cart**: Logged-in users can add products to their cart, view their cart, and place orders.
- **Order Management**: Users can place orders for the products in their shopping cart.

## Technology Stack

- **Python**: Backend logic is implemented using Python.
- **SQLite**: Data is persisted in an SQLite database for easy setup and lightweight storage.
- **Utils Module**: Utility functions for database connection and password hashing.
- **Poetry**: Dependency management is handled using Poetry.

## Setup Instructions

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```
2. Install Poetry:
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```
3. Install the required dependencies using Poetry:
   ```bash
   poetry install
   ```
4. Initialize the database:
   ```bash
   poetry run python -c "from utils import init_db; init_db()"
   ```
5. Run the application:
   ```bash
   poetry run python main.py
   ```

## Running Unit Tests

1. To run the unit tests, use the following command:
   ```bash
   poetry run python -m unittest discover tests
   ```

## Usage

- **User Registration**: A user can register by providing a unique username and password.
- **User Login**: Users can log in with their credentials to manage their account and interact with the product catalog.
- **Admin Functions**: Admin users have the ability to add, edit, or remove products.
- **Shopping Cart**: Users can add products to their cart and view the cart contents.
- **Placing Orders**: Users can place orders for items in their cart.

## Example Usage

```python
# User Registration
user = User("john_doe", "password123")
user.register()

# User Login
logged_in_user = User.login("john_doe", "password123")
if logged_in_user:
    # Add Product (Admin Only)
    if logged_in_user.is_admin:
        product_repo = ProductRepository(get_db_connection())
        product_repo.add_product("Laptop", "Gaming Laptop", 1500.0)

    # View Products
    products = product_repo.view_products()
    for product in products:
        print(product)

    # Add to Cart
    cart = Cart(user_id=1, connection=get_db_connection())
    cart.add_to_cart(product_id=1, quantity=2)

    # View Cart
    cart_items = cart.view_cart()
    print(cart_items)

    # Place Order
    cart.place_order()
```

## Improvements

- **Code Refactoring**: ProductRepository methods should not be called statically in the example usage; an instance should be created.
- **Connection Management**: Pass database connection objects correctly to avoid runtime issues.
- **Exception Handling**: Improve the granularity of exception handling for more informative error messages.

## License

This project is licensed under the MIT License.
