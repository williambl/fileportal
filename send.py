import socket

def send(ip, path):
    f = open(path, 'rb')

    s = socket.socket()
    s.bind(('', 25565))
    s.listen(5)

    csocket, addr = s.accept()
    print('Got connection from', addr)

    while True:
        data = f.read(1024)
        if (len(data)):
            csocket.send(data)
        else:
            break

            f.close()
            csocket.close()
