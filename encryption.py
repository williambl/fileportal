from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.fernet import Fernet
import tempfile
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

    return get_key().public_key()

def encrypt(public_key, message):
    return public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None
        )
    )

def decrypt(private_key, message):
    return private_key.decrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA1()),
            algorithm=hashes.SHA1(),
            label=None
        )
    )

def get_fernet_key():
    return Fernet.generate_key()

def encrypt_file(key, f):
    text = f.read()
    fnt = Fernet(key)
    encrypted = fnt.encrypt(text)
    tf = tempfile.TemporaryFile()
    tf.write(encrypted)
    tf.seek(0)
    return tf

def decrypt_file(key, f):
    encrypted = f.read()
    decrypt_fernet(key, encrypted)
    tf = tempfile.NamedTemporaryFile()
    tf.write(encrypted)
    tf.seek(0)
    return tf

def decrypt_fernet(key, token):
    fnt = Fernet(key)
    return fnt.decrypt(token)
