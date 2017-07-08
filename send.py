from hashlib import sha256
import socket
import json
import sys
import os
import encryption
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend

def send(path):

    s = socket.socket()
    s.bind(('', 25565))
    s.listen(5)

    csocket, addr = s.accept()
    print('Got connection from', addr)

    public_key_encoded = csocket.recv(1024)

    public_key = serialization.load_pem_public_key(public_key_encoded, default_backend())

    with open(path, 'rb') as f:
        metadata = {'filename': os.path.basename(path), 'size': os.path.getsize(path),
                    'checksum': sha256(f.read()).hexdigest()}
    metajson = json.dumps(metadata)
    print(metajson)

    encryptedmetajson = encryption.encrypt(public_key, metajson.encode('utf-8'))

    csocket.send(encryptedmetajson)

    f = open(path, 'rb')

    while True:
        message = csocket.recv(1024).decode('utf-8')
        if (message == "send it"):
            break
        elif (message == "nosend"):
            f.close()
            csocket.close()
            sys.exit()

    while True:
        data = f.read(1024)
        if (len(data)):
            csocket.send(encryption.encrypt(public_key, data))
        else:
            break

            f.close()
            csocket.close()
