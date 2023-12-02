import secrets
import string

import bcrypt


def generate_hash(password_str: str):
    # Generate a salt
    salt = bcrypt.gensalt()
    # Generate the hash
    hashed = bcrypt.hashpw(password_str.encode('utf-8'), salt)
    return hashed.decode('utf-8')


def generate_api_key(length=64):
    safe_punctuation = ''  # '!#$%&*+-=@'
    characters = string.ascii_letters + string.digits + safe_punctuation
    secure_key = ''.join(secrets.choice(characters) for i in range(length))
    return secure_key


api_key = generate_api_key(48)
print("API... Key:", api_key)
print("Hashed Key:", generate_hash(api_key))
