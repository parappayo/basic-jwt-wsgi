import hashlib, uuid


def encode(password):
    password_salt = uuid.uuid4().bytes
    password_hash = hashlib.blake2b(password.encode('utf-8'), salt=password_salt)
    return password_salt, password_hash.digest()


def validate(password, password_salt, password_hash):
    validate_hash = hashlib.blake2b(password.encode('utf-8'), salt=password_salt)
    return validate_hash.digest() == password_hash
