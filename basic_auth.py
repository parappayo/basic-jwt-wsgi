import base64


def decode(auth_key):
    return base64.b64decode(auth_key).decode('ascii').split(':')
