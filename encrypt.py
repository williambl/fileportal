from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import os

def new_key():
    key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )

    os.mkdir(os.path.expanduser('~/.fileportal/'))

    with open(os.path.expanduser('~/.fileportal/key_rsa.pem'), "wb") as f:
        f.write(key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.BestAvailableEncryption(b"passphrase")
        ))

    return key

def get_key():
    if (not os.path.exists(os.path.expanduser('~/.fileportal/key_rsa.pem'))):
        return None

    if (key):
        return key

    with open(os.path.expanduser('~/.fileportal/key_rsa.pem'), "rb") as f:
        key = serialization.load_pem_private_key(
            f.read(),
            password=b"passphrase",
            backend=default_backend()
        )

    return key

def get_public_key():
    if (not os.path.exists(os.path.expanduser('~/.fileportal/key_rsa.pem'))):
        return None

    return key.public_key()