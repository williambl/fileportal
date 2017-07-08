from hashlib import sha256
import socket
import json
import sys
import os

def send(ip, path):

    s = socket.socket()
    s.bind(('', 25565))
    s.listen(5)

    csocket, addr = s.accept()
    print('Got connection from', addr)

    with open(path, 'rb') as f:
        metadata = {'filename': os.path.basename(path), 'size': os.path.getsize(path),
                    'checksum': sha256(f.read()).hexdigest()}
    metajson = json.dumps(metadata)
    print(metajson)

    csocket.send(metajson.encode('utf-8'))

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
            csocket.send(data)
        else:
            break

            f.close()
            csocket.close()
