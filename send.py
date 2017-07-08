import socket
import json
import sys

def send(ip, path):
    f = open(path, 'rb')

    s = socket.socket()
    s.bind(('', 25565))
    s.listen(5)

    csocket, addr = s.accept()
    print('Got connection from', addr)

    metadata = {'filename': f.name, 'size': str(f.__sizeof__())}
    metajson = json.dumps(metadata)
    print(metajson)

    csocket.send(metajson.encode('utf-8'))

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
