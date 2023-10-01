import bcrypt


def generate_hash(password_str: str):
    # Generate a salt
    salt = bcrypt.gensalt()
    # Generate the hash
    hashed = bcrypt.hashpw(password_str.encode('utf-8'), salt)
    return hashed.decode('utf-8')
