from send import send
from recv import recv

print("Welcome to fileportal!")

response = input("Send or recv?")

if (response.upper() in ["SEND", "S"]):
    path = input("Which file?")
    send(path)
elif (response.upper() in ["RECV", "RECEIVE", "R"]):
    ip = input("Where from?")
    recv(ip)
