import socket

def recv(ip, path):
    s = socket.socket()

    s.bind((ip, 25565))

    f = open(path, 'wb')

    s.listen(5)

    csocket, addr = s.accept()
    print('Got connection from', ip)

    while True:
        data = csocket.recv(1024)
        if (len(data)):
            f.write(data)
        else:
            break

            f.close()
            csocket.close()
