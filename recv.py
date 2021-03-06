from hashlib import sha256
import socket
import hashlib
import json
import sys
import encryption
from cryptography.hazmat.primitives import serialization
from hurry import filesize

def recv(ip):
    private_key = encryption.get_key()
    u = upnp_handler.new_upnp()
    upnp_handler.forward_port(u, 25565)

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
    fernet_key = metadata['fernet_key'].encode('utf-8')


    if (input("Recieve " + filename + ", a " + filesize.size(
        size, system = filesize.alternative) + "byte file? [Y/n] \n").upper() in
        ['N', 'NO']):
        
        print('Abort.')
        s.send("nosend".encode('utf-8'))
        upnp_handler.close_port(u, 25565)
        sys.exit()



    s.send("send it".encode('utf-8'))

    encryptedtoken = b""

    while True:
        data = s.recv(1024)
        if (len(data)):
            encryptedtoken += data
        else:
            break

            s.close()
            upnp_handler.close_port(u, 25565)

    with open(filename, 'w+b') as f:
        f.truncate(0)
        f.write(encryption.decrypt_fernet(fernet_key, encryptedtoken))

    f = open(filename, 'rb')
    if (sha256(f.read()).hexdigest() != checksum):
        print("WARNING! Something happened to the file! Checksums do not match!")
        print(sha256(repr(f.read).encode('utf-8')).hexdigest())
