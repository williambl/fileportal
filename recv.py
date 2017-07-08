from hashlib import sha256
import socket
import hashlib
import json
import sys

def recv(ip):
    s = socket.socket()

    s.connect((ip, 25565))

    metajson = s.recv(1024).decode('utf-8')
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
            f.write(data)
        else:
            break

            f.close()
            s.close()

    f = open(filename, 'rb')
    if (sha256(f.read()).hexdigest() != checksum):
        print("WARNING! Something happened to the file! Checksums do not match!")
        print(sha256(repr(f.read).encode('utf-8')).hexdigest())
