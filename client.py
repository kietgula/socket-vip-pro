from tkinter import *
from tkinter import Tk
import tkinter
import socket
import json
from datetime import date


FORMAT = "utf8"

window=Tk()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

def main_window():
    global window
    window.destroy()
    window=Tk()
    window.geometry("216x216")
    
    Login_button=Button(window, text="Sign out", command=login_window)
    Login_button.place(x=110,y=50)
    
    intro_lb=Label(window, text="Click on currency tab\n on the left side \nfor your information").place(x=80,y=80)
 
    
    #Tạo 7 button tiền tệ
    AUD_button=Button(window,text="AUD", command=lambda: getMoney("AUD"))
    AUD_button.grid(column=0,row=1)
    CAD_button=Button(window,text="CAD", command=lambda: getMoney("CAD"))
    CAD_button.grid(column=0,row=2)
    CHF_button=Button(window,text="CHF", command=lambda: getMoney("CHF"))
    CHF_button.grid(column=0,row=3)
    EUR_button=Button(window,text="EUR", command=lambda: getMoney("EUR"))
    EUR_button.grid(column=0,row=4)
    GBP_button=Button(window, text="GBP", command=lambda: getMoney("GBP"))
    GBP_button.grid(column=0, row=5)
    JPY_button=Button(window, text="JPY", command=lambda: getMoney("JPY"))
    JPY_button.grid(column=0, row=6)
    USD_button=Button(window, text="USD", command=lambda: getMoney("USD"))
    USD_button.grid(column=0, row=7)
    
    #Tạo Button ngắt kết nối
    disconnect_button=Button(window, text="Disconnect", command = disconnect)
    disconnect_button.place(x=110, y=10)

def disconnect():
    global s 
    global window
    offline_lb=Label(window, text="offline").place(x=62,y=11)
    hide_info_money=Label(window, text="                          \n                           \n                      \n                         ").place(x=80, y=80)
    s.sendall("disconnect".encode(FORMAT))
    

def getMoney(name):
    global Info
    try:
        global window
        global s 
        s.sendall("get data".encode(FORMAT)) #0
        s.recv(1024) #3
        s.sendall(name.encode(FORMAT)) #4
        data = s.recv(1024).decode(FORMAT) #7
        
        Info = Label(window, text = data, border=16).place(x=80,y=80)
    except:
        hide_info_money=Label(window, text="                          \n                           \n                      \n                         ").place(x=80, y=80)
        Info = Label(window, text = "Disconnected").place(x=80,y=80)
    today = date.today()
    time_lb=Label(window, text=today).place(x=55, y=182)
    
 
def login_check(username, password):
    global window
    global s
    try:
        s.sendall("login".encode(FORMAT))
        s.recv(1024)                        #3 
        s.sendall(username.encode(FORMAT)) #4 gửi username
        s.recv(1024)
        s.sendall(password.encode(FORMAT))
        s.recv(1024).decode(FORMAT) #nhan got password
        s.sendall("Result?".encode(FORMAT))
        result=s.recv(1024).decode(FORMAT)
        print(result)
        
        if result=='1':
            main_window()
        else:
            fail=Label(text="Login Fail").grid(column=1,row=1)
    except:
        fail=Label(text="Disconnected").grid(column=1,row=1)
        
    
        
def register_check(username, password):
    global window
    global s
    try:
        s.sendall("register".encode(FORMAT)) #0 gửi register
        s.recv(1024)                        #3 
        s.sendall(username.encode(FORMAT)) #4 gửi username
        s.recv(1024)
        s.sendall(password.encode(FORMAT))
        temp=s.recv(1024).decode(FORMAT) #nhan got password
        s.sendall("Result?".encode(FORMAT))

        result=s.recv(1024).decode(FORMAT)
        
        if result=='1':
            login_window()
        else:
            fail=Label(text="Register Fail").grid(column=1,row=1)
    except:
        fail=Label(text="Disconnected").grid(column=1,row=1)
        
    
 
def login_window():
    global window
    global login_screen_photo
    window.destroy()
    window=Tk()
    window.geometry("1280x720")
    #add ảnh vào cửa sổ
    login_screen_photo=PhotoImage(file="login_screen.png")
    Label(window, image=login_screen_photo, bg="black").place(x=0, y=0)
 
      #tạo 2 cái text box username với password
    username_tb=Entry(window, text="enter your username", bg="white", fg="black", font=("Roboto", 24), bd=0, width=26)
    username_tb.place(x=426, y=313)
    password_tb=Entry(window, text="enter your password", bg="white", fg="black", font=("Roboto", 24), bd=0, width=26)
    password_tb.place(x=426, y=460)
 
    #tạo button Login
    #tạo button NEXT
    next_button=Button( window, text="Next",fg="white", font=("Roboto", 11, "bold"), bd=0, bg="#1a73e8", height=2, width=11, command=lambda: login_check(username_tb.get(), password_tb.get())).place(x=809,y=580)
    
    #tạo button Create Account
    create_account_button=Button(window, text="Create Account",fg="#1a73e8", font=("Roboto", 12, "bold"), bd=0, bg="white", height=3, width=16, command=register_window).place(x=401,y=570)
 
def register_window():
    global window
    global register_screen_photo
    window.destroy()
    window=Tk()
    window.geometry("1280x720")
    register_screen_photo=PhotoImage(file="register_screen.png")
    #add ảnh vào cửa sổ
    Label(window, image=register_screen_photo, bg="black").place(x=0, y=0)
     #tạo 2 cái text box username với password
    username_tb=Entry(window, text="enter your username")
    username_tb.place(x=426, y=313)
    password_tb=Entry(window, text="enter your password")
    password_tb.place(x=426, y=460)
 
    #tạo button register
    Register_button=Button(window,text="register", command=lambda: register_check(username_tb.get(), password_tb.get())).place(x=809,y=580) 
    
    #button ve man hinh login
    Login_button=Button(window, text="Go back to Login", command=login_window)
    Login_button.grid(column=10,row=10)
 
def ip_check(ip, port):
    global window
    global s
    try:
        s.connect((ip, int(port)))
        login_window()
    except:
        connectFail_lb=Label(window, text="fail connect").grid(column=0, row=3)
        print(ip)
        print(port)
         
 
def start_window():
    global window
    window.geometry("256x128")
    #ip_server=Label(window, text="ip").grid(column)
    host_entry=Entry(window, text="enter host ip")
    host_entry.grid(column=0,row=1)
    
    ip_lb=Label(window, text="ip").grid(column=0,row=0)
    be_lb=Label(window, text=":").grid(column=1,row=1)
    port_lb=Label(window,text="port").grid(column=2,row=0)
    
    port_entry=Entry(window, text="enter port")
    port_entry.grid(column=2,row=1)
    
    connect_button=Button(text="connect", fg="black", command=lambda:ip_check(host_entry.get(), port_entry.get()))
    connect_button.grid(column=0,row=2)
    
    
 
 
start_window()
input()
mainloop()

