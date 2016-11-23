from Tkinter import *
import socket
import sys
import tkMessageBox

#inisialisasi
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#koneksi
server_address = ('localhost', 11001)
client_socket.connect(server_address)

def onClose():
        
    message = "logout"
    #client_socket.sendall(message)
    #data = client_socket.recv(1024)
    #data = data.strip().split()
    
    message = "exit"
    #client_socket.sendall(message)
    #data = client_socket.recv(1024)
    #data = data.strip().split()
    
    print >>sys.stderr, 'onCLose'
    return 1

def showDashboard(username):
    top = Tk()    

def controlLogin(master):
    frames = master.winfo_children()
    widgets = frames[0].winfo_children()    
    username = widgets[1].get()
    widgets = frames[1].winfo_children()
    password = widgets[1].get()
    print >>sys.stderr, 'message: '+username
    print >>sys.stderr, 'password: '+password
    
    message = 'login '+username+' '+password
    client_socket.sendall(message)
    data = client_socket.recv(1024)
    data = data.strip().split()
    if data[1] in ['100']:
        master.destroy()
        showDashboard(username)
    elif data[1] in ['243']:
        tkMessageBox.showinfo("Error", "Akun \""+username+"\" telah login")
    elif data[1] in ['241']:
        tkMessageBox.showinfo("Error", "Akun \""+username+"\" tidak terdaftar")
    elif data[1] in ['242']:
        tkMessageBox.showinfo("Error", "Password akun \""+username+"\" salah")

    return 1
    

def showLogin(master):
    master.destroy()    
    top = Tk()
    top.title("Login")
    top.minsize(250, 75)
    top.maxsize(250, 75)    
    top.protocol("WM_DELETE_WINDOW", onClose)    
    
    frame = Frame(top)
    frame.pack()
    bottomFrame = Frame(top)
    bottomFrame.pack(side = TOP)
    buttonFrame = Frame(top)
    buttonFrame.pack(side = TOP)
    
    L1 = Label(frame, text="User Name", width=10)
    L1.pack( side = LEFT)
    E1 = Entry(frame, bd =2)
    E1.pack(side = LEFT)
    
    L2 = Label(bottomFrame, text="Password", width=10)
    L2.pack( side = LEFT)
    E2 = Entry(bottomFrame, bd =2)
    E2.pack(side = LEFT)
    
    connectButton = Button(buttonFrame, text=("Connect"), font=("Calibri", 9), command=lambda: controlLogin(top)) 
    connectButton.pack()  
    top.mainloop()
    
    
def showHome():
    top = Tk()
    top.title("Chat EK-2")
    top.minsize(200, 150)
    top.maxsize(200, 150)        
    #top.protocol("WM_DELETE_WINDOW", onClose)    
        
    frameFill = Frame(top, height=30)
    frameFill.pack()
        
    frameLogin = Frame(top)
    frameLogin.pack()
    frameRegister = Frame(top)
    frameRegister.pack(side = TOP)    
    
    loginButton = Button(frameLogin, text="Login", width=10, height=2, font=("Calibri", 9), command=lambda: showLogin(top))
    loginButton.pack(side = TOP)
    registerButton = Button(frameRegister, text="Register", width=10, height=2,font=("Calibri", 9))
    registerButton.pack(side = TOP)    
    
    top.mainloop()

showHome()