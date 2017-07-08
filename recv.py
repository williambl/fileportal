import socket

def recv(ip):
    s = socket.socket()

    s.connect((ip, 25565))

    filename = s.recv(1024)

    f = open(filename.decode('utf-8'),'wb')

    s.send("send it".encode('utf-8'))

    while True:
        data = s.recv(1024)
        if (len(data)):
            f.write(data)
        else:
            break

            f.close()
            s.close()
