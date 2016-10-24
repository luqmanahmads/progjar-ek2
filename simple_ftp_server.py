import threading
import socket
import sys
import commands
import time
import string
import os

#global variable
listCommand = ['cd', 'retr', 'list', 'put', 'del', 'exit', 'user', 'pass']

#inisialisasi
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print >>sys.stderr, "Creating TCP socket successful..."

#binding socket ke address:port
server_address = ('localhost', 11001)
print >>sys.stderr, "Binding to %s port %s successful..." % server_address
sock.bind(server_address)

#listening
sock.listen(1)

#loading user and pass from text file
user_name = ["luqman", "ahmad","aditya","gunawan", "delia", "dedell", "adel"]
user_pass = ["123", "321","456","tralala", "cantik", "lucu", "pelangi"]
user_auth = [0, 0, 0, 0, 0, 0, 0]
user_add = [0, 0, 0, 0, 0, 0, 0]	
print >>sys.stderr, "Loading user information..."
print >>sys.stderr, "Starting up server...\n"
print >>sys.stderr, "WELCOME TO SIMPLE FTP SERVER"

#fungsi untuk login user
def login(username,password,alamat_client):
    if username in user_name:
        index = user_name.index(username)
        if password == user_pass[index]:
            user_add[index] = alamat_client[0]
            user_auth[index] = 1
            return "[OK] login berhasil"
        else:
            return "[ERR] password salah"
    else:
        return "[ERR] username tidak ditemukan"

#fungsi untuk autentifikasi client
def authenticate(alamat_client):
    if alamat_client[0] in user_add:
        return 1
    else:
        return 0
    
#fungsi multithread untuk  client
def service(koneksi_client,alamat_client):
    try:
        print >>sys.stderr, "ada koneksi dari client ", alamat_client[0]
        username = ""
        password = ""
        while True:
            koneksi_client.send("\n>>")
            command = koneksi_client.recv(1024)
            
            #pengecekan autentikasi
            command = command.strip().split()
            command[0] = command[0].lower()
            
            if command[0] in listCommand:
                if command[0] in ['user']:
                    if len(command) == 2:
                        username = command[1]
                        message = "[OK] username berhasil direkam"
                    else:
                        message = "[ERR] penggunaan :>> user your_username"
                if command[0] in ['pass']:
                    if len(command) == 2:
                        password = command[1]
                        message = login(username,password,alamat_client)
                    else:
                        message = "[ERR] penggunaan :>> pass your_password"
                if command[0] in ['cd', 'retr', 'list', 'put', 'del', 'exit']:
                    if authenticate(alamat_client) == 1:
                        if command[0] in ['list']:
                            if len(command) == 1:
                                message = commands.getoutput("ls -al")
                        if command[0] in ['cd']:
                            if len(command) == 2:
                                try:
                                    os.chdir(cmd[-1])
                                except:
                                    message = "[ERROR] direktori tidak ada"
                                else:
                                    message = "[OK] direktori sekarang " + os.getcwd()
                            else:
                                message = "[ERR] penggunaan :>> cd intended_directory"
                        if command[0] in ['del']:
                            if len(command) == 2:
                                message = commands.getoutput('rm ' + command[1])
                                if message == "":
                                    message = "File " + command[1] + " telah dihapus"
                            else:
                                message = "[ERR] penggunaan :>> del file_name"
                        if command[0] in ['exit']:
                            index = user_add.index(alamat_client[0])
                            user_add[index] = 0
                            user_auth[index] = 0
                            break
                        if command[0] in ['retr']:
                            if len(command) == 2:
                                f = open(command[1], "rb")
                                buff = f.read(1024)
                                while (buff):
                                    koneksi_client.send(buff)
                                    buff = f.read(1024)
                                f.close()
                                message = "[OK] file telah terdownload"
                            else:
                                message = "[ERR] penggunaan :>> retr file_name" 
                        if command[0] in ['put']:
                            if len(command) == 2:
                                f = open(command[1], "wb")
                                if f:
                                    buff = koneksi_client.recv(1024)
                                    f.write(buff)
                                    koneksi_client.send("receiving file..\n")
                                    f.close()
                                    message = "[OK] file telah terupload"
                                else:
                                    message = "[ERR] gagal membuat file. gunakan nama file lain."
                            else:
                                message = "[ERR] penggunaan :>> put nama_file"
                    else:
                        message = "[ERR] anda belum terautentikasi"
                    
            else:
                    message = "[ERR] command tidak ditemukan"
                
                
            koneksi_client.send(message)
    finally:
        koneksi_client.close()
        

while True:
    #waiting for connection
    print >>sys.stderr, "waiting for connection"
    koneksi_client, alamat_client = sock.accept()
    s= threading.Thread(target=service, args=(koneksi_client, alamat_client))
    s.start()
