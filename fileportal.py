from send import send
from recv import recv
from encryption import *

if (not key_exists()):
    new_key()

print("Welcome to fileportal!")

response = input("Send or recv?")

if (response.upper() in ["SEND", "S"]):
    path = input("Which file?")
    send(path)
elif (response.upper() in ["RECV", "RECEIVE", "R"]):
    ip = input("Where from?")
    recv(ip)
