# app/utils/security.py
import hashlib
import os


def hash_password(password: str) -> str:
    # Generate a random salt
    salt = os.urandom(16)  # 16 bytes salt
    # Hash the password with the salt
    hashed_password = hashlib.pbkdf2_hmac(
        'sha256',  # The hash digest algorithm
        password.encode('utf-8'),  # The password to hash
        salt,  # The salt
        100000  # Number of iterations
    )
    # Return the salt and hashed password together
    return salt.hex() + ':' + hashed_password.hex()


def verify_password(stored_password: str, provided_password: str) -> bool:
    salt, hashed_password = stored_password.split(':')
    salt = bytes.fromhex(salt)
    # Hash the provided password using the same salt
    hashed_provided_password = hashlib.pbkdf2_hmac(
        'sha256',
        provided_password.encode('utf-8'),
        salt,
        100000
    ).hex()
    # Check if the hashes match
    return hashed_password == hashed_provided_password
