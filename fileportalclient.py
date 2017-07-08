import socket

s = socket.socket()
s.connect((socket.gethostname(), 25565))


f = open('send','rb')

while True:
    print('Sending...')
    data = f.read(1024)
    if (len(data)):
        s.send(data)
    else:
        break

f.close()
s.close()
