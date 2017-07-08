from send import send
from recv import recv

print("Welcome to fileportal!")

response = input("Send or recv?")

if (response == "send"):
    path = input("Which file?")
    ip = input("Where to?")
    send(ip, path)
elif (response == "recv"):
    ip = input("Where from?")
    recv(ip, path)
