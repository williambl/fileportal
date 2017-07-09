from hashlib import sha256
import socket
import json
import sys
import os
import encryption
from io import StringIO
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
import upnp_handler

def send(path):
    fernet_key = encryption.get_fernet_key()
    u = upnp_handler.new_upnp()
    upnp_handler.forward_port(u, 25565)

    s = socket.socket()
    s.bind(('', 25565))
    s.listen(5)

    csocket, addr = s.accept()
    print('Got connection from', addr)

    public_key_encoded = csocket.recv(1024)

    public_key = serialization.load_pem_public_key(public_key_encoded, default_backend())

    with open(path, 'rb') as f:
        metadata = {'filename': os.path.basename(path),
                    'size': os.path.getsize(path),
                    'checksum': sha256(f.read()).hexdigest(),
                    'fernet_key': fernet_key.decode('utf-8')}
    metajson = json.dumps(metadata)
    print(metajson)

    encryptedmetajson = encryption.encrypt(public_key, metajson.encode('utf-8'))

    csocket.send(encryptedmetajson)

    with open(path, 'rb') as f:
        token = encryption.encrypt_file(fernet_key, f)

    while True:
        message = csocket.recv(1024).decode('utf-8')
        if (message == "send it"):
            break
        elif (message == "nosend"):
            f.close()
            csocket.close()
            upnp_handler.close_port(u, 25565)
            sys.exit()

    while True:
        data = token.read(1024)
        if (len(data)):
            csocket.send(data)
        else:
            break

            token.close()
            csocket.close()
            upnp_handler.close_port(u, 25565)
