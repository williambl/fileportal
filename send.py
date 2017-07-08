import socket

def send(ip, path):
    s = socket.socket()
    s.connect((ip, 25565))


    f = open(path,'rb')

    while True:
        print('Sending...')
        data = f.read()
        if (len(data)):
            s.send(data)
        else:
            break

            f.close()
            s.close()
