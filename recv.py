import socket

def recv(ip, path):
    s = socket.socket()

    s.connect((ip, 25565))

    f = open(path,'wb')

    while True:
        data = s.recv(1024)
        if (len(data)):
            f.write(data)
        else:
            break

            f.close()
            s.close()
