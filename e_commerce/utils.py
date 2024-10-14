import hashlib

def hash_password(password: str) -> str:
    """
    Hashes the password using SHA-256.
    
    :param password: The plain text password to be hashed.
    :return: The hashed password as a hexadecimal string.
    """
    return hashlib.sha256(password.encode()).hexdigest()
