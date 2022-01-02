import socket
import threading
import json
import requests
from tkinter import *
from tkinter import Tk
import tkinter
#from requests.api import request
 
HOST = "127.0.0.1"
PORT  = 65432
FORMAT = "utf8"
window =Tk()
#------------------------------------
 

def add_User(username, password):
    with open('data_User.js') as json_file:
        data = json.load(json_file)
    data.append({
        'username': username,
        'password': password
    })
    
    with open('data_User.js', 'w') as outfile:
        json.dump(data, outfile)
 
def check_Available_User(username):
    print("Dang check")
    with open('data_User.js') as json_file:
        data=json.load(json_file)
        for user in data:
            if (username==user["username"]):
                return '0'
    return '1'

def check_Login(username, password):
    with open('data_User.js') as json_file:
        data=json.load(json_file)
        for user in data:
            if (username==user["username"] and password==user["password"]):
                return '1'
    return '0'
        
 
#-----------------------------------
 
def login(conn : socket, addr):
    conn.sendall("got login".encode(FORMAT)) #2 gửu đã nhận được login
    username=conn.recv(1024).decode(FORMAT) #5 
    conn.sendall("got username".encode(FORMAT)) #6 
    password=conn.recv(1024).decode(FORMAT) 
    conn.sendall("got password".encode(FORMAT))
    conn.recv(1024).decode(FORMAT) #nhan result?
    result=check_Login(username,password)
    conn.sendall(result.encode(FORMAT))
 
#----------------------------------------------------------
 
def getDataAPI():
    key = requests.get("https://vapi.vnappmob.com/api/request_api_key?scope=exchange_rate")
    key = 'Bearer '+key.json()['results']
    header = {
        'Accept': 'application/json',
        'Authorization': key
        }
    data = requests.get("https://vapi.vnappmob.com/api/v2/exchange_rate/sbv", headers = header)
    return data.json()
 
def getMoneyData(moneyName):
    data = getDataAPI()
    for money in data["results"]:
        if money["currency"]==moneyName:
            return money
    return "none"

def getData(conn : socket, addr):
    conn.sendall("got data".encode(FORMAT)) #2
    name = conn.recv(1024).decode(FORMAT) #5
    
    data = getMoneyData(name)
    #{'buy': 18464.0, 'currency': 'CAD', 'sell': 19606.0}
    Name = name
    Buy = str(data["buy"])
    Sell = str(data["sell"])
    
    msg = "currency: "+ Name +"\n Buy: "+ Buy + "vnđ\n Sell: "+ Sell +"vnđ"
    
    conn.sendall(msg.encode(FORMAT)) #6

    
#----------------------------------------------------------
 
def register(conn:socket, addr):
    conn.sendall("got register".encode(FORMAT)) #2 gửu đã nhận được register
    username=conn.recv(1024).decode(FORMAT) #5 
    conn.sendall("got username".encode(FORMAT)) #6 
    password=conn.recv(1024).decode(FORMAT) 
    conn.sendall("got password".encode(FORMAT))
    conn.recv(1024).decode(FORMAT) #nhan result?
    result=check_Available_User(username)
    conn.sendall(str(result).encode(FORMAT))
    
    if result=='1':
        add_User(username,password)
    
 
def Client(conn:socket, addr):
    global window
    global disconnect
    while True:
        try:
            # print(addr," connected")
            direction = conn.recv(1024).decode(FORMAT) #1
            if direction == "register": 
                register(conn, addr)
            if direction == "login":
                login(conn, addr)
            if direction == "get data":
                getData(conn, addr)
            if direction== "disconnect":
                conn.close()
            if disconnect==1:
                conn.close()
        except:
            return 
    return 1
 
def createThread():
    global s
    s.listen()  
    while(1):
        print("Waiting...\n")
        conn, addr = s.accept()
        thr = threading.Thread(target=Client, args=(conn, addr))
        thr.daemon = True
        thr.start()
 
#------------------MAIN----------------------
def disconnect():
    global disconnect
    global window
    if disconnect==1:
        disconnect=0
        online=Label(window, text="Online").grid(row=1, column=1)
    else: 
        disconnect=1
        offline=Label(window, text="Offline").grid(row=1, column=1)


def main():
    global disconnect
    window.geometry("256x128")
    global s
    s.bind((HOST, PORT))
    thr = threading.Thread(target=createThread)
    thr.daemon = True
    thr.start()
    online=Label(window, text="Online").grid(row=1, column=1)


    exit_button=Button(text="Offline/Online", command=disconnect)
    exit_button.place(relx=0.5, rely=0.5, anchor=CENTER)
#-----------------------------
 
s  = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
main()
window.mainloop()
print("finish")
input()

