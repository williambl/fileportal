import socket

def send(ip, path):
    f = open(path, 'rb')

    s = socket.socket()
    s.bind(('', 25565))
    s.listen(5)

    csocket, addr = s.accept()
    print('Got connection from', addr)

    csocket.send(f.name.encode('utf-8'))

    while True:
        if (csocket.recv(1024).decode('utf-8') == "send it"): break

    while True:
        data = f.read(1024)
        if (len(data)):
            csocket.send(data)
        else:
            break

            f.close()
            csocket.close()
