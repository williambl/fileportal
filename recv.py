from hashlib import sha256
import socket
import hashlib
import json
import sys
import encryption
from cryptography.hazmat.primitives import serialization

def recv(ip):
    private_key = encryption.get_key()

    s = socket.socket()

    s.connect((ip, 25565))

    public_key = encryption.get_public_key()

    s.send(public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ))

    encryptedmetajson = s.recv(1024)
    metajson = encryption.decrypt(private_key, encryptedmetajson).decode('utf-8')
    metadata = json.loads(metajson)
    filename = metadata['filename']
    size = metadata['size']
    checksum = metadata['checksum']

    f = open(filename, 'wb')

    if (input("Recieve " + filename + ", a " + str(size) + "byte file? [Y/n] \n").upper()
        in ['N', 'NO']):
        print('Abort.')
        s.send("nosend".encode('utf-8'))
        sys.exit()



    s.send("send it".encode('utf-8'))

    while True:
        data = s.recv(1024)
        if (len(data)):
            f.write(encryption.decrypt(private_key, data))
        else:
            break

            f.close()
            s.close()

    f = open(filename, 'rb')
    if (sha256(f.read()).hexdigest() != checksum):
        print("WARNING! Something happened to the file! Checksums do not match!")
        print(sha256(repr(f.read).encode('utf-8')).hexdigest())
