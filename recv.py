import socket

def recv(ip, path):
    s = socket.socket()

    s.bind(('', 25565))

    f = open(path, 'wb')

    s.listen(5)

    csocket, addr = s.accept()
    print('Got connection from', addr)

    while True:
        data = csocket.recv()
        if (len(data)):
            f.write(data)
        else:
            break

            f.close()
            csocket.close()
