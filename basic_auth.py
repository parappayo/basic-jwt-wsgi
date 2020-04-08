import base64


def decode(auth_key):
    return base64.b64decode(auth_key).decode('ascii').split(':')


def decode_header(auth_header):
    auth_header_prefix = 'basic '
    if not auth_header.lower().startswith(auth_header_prefix):
        return False, False
    return decode(auth_header[len(auth_header_prefix):])
