import threading
import socket
import sys
import time
import string

#inisialisasi
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print >>sys.stderr, "Creating TCP socket successfil..."

#binding socket to address:port
server_address = ('localhost', 11003)
print >>sys.stderr, "Binding to %s port %s successful..." % server_address
sock.bind(server_address)

#listening
sock.listen(1)

#commandlist
listCommand = ['login', 'logout', 'send']
userid = ['100', '101', '102']
username = ['luqman', 'adit', 'delia', 'tion']
userpass = ['123', '123', '123', '123']
useraddr = []
usersock = []

#fungsi untuk logout
def logout():
    return "a"

#fungsi untuk login user
def login(client_username, client_password, koneksi_client, alamat_client):
    if client_username in username:
        index = username.index(client_username)
        if client_password == userpass[index]:
            useraddr.insert(index, alamat_client)
            usersock.insert(index, koneksi_client)
            return "SUKSES : login berhasil\n"
        else:
            return "GAGAL : password salah\n"
    else:
        return "GAGAL : username tidak ditemukan\n"

#fungsi auntentikasi
def authenticate(alamat_client):
    if [item for item in useraddr if item[0] == alamat_client[0]]:
        return 1
    else:
        return 0

#fungsi untuk mengirim pesan
def kirim(username_pengirim, username_penerima, pesan):
    if username_penerima in username:
        index = username.index(username_penerima)
        n = len(usersock)
        if index < n:
            usersock[index].send("["+username_pengirim+"] "+pesan+"\n")
            return "SUKSES : pesan terkirim\n"
        else:
            return "GAGAL : penerima tidak online\n"
    else:
        return "GAGAL : username penerima tidak tersedia\n"

#fungsi untuk melayani servis client
def service(koneksi_client, alamat_client):
    try:
        print >>sys.stderr, "ada koneksi dari client ", alamat_client[0]
        client_username = ""
        client_password = ""
        while True:
            command = koneksi_client.recv(1024)
            command = command.strip().split()
            command[0] = command[0].lower()
            
            message = command[0]            
            
            if command[0] in listCommand:            
                
                if command[0] in ['login']:
                    if len(command) == 3:
                        client_username = command[1]
                        client_password = command[2]
                        message = login(client_username, client_password, koneksi_client, alamat_client)
                    else:
                        message = "GAGAL : syntax error\n"
                
                elif command[0] in ['logout', 'send']:
                    if authenticate(alamat_client) == 1:
                        if command[0] in ['send']:
                            if len(command) == 3:
                                message = kirim(client_username, command[1], command[2])
                            else:
                                message = "GAGAL : penggunaan [send] [user_pengirim] [pesan]"
                        if command[0] in ['logout']:
                            if len(command) == 1:
                                message = logout()
                            else:
                                message = "GAGAL : syntax error\n"
                    else:
                        message = "GAGAL : anda tidak terautentikasi"
                    
                else:
                    message = "GAGAL\n"
            else:
                message = "GAGAL : command tidak tersedia\n"
            koneksi_client.send(message)
    finally:
        koneksi_client.close()
    
while True:
    #waiting for connection
    print >>sys.stderr, "waiting for connection"
    koneksi_client, alamat_client = sock.accept()
    #print >>sys.stderr, alamat_client[0]
    #print >>sys.stderr, alamat_client[1]
    s = threading.Thread(target=service, args=(koneksi_client, alamat_client))
    s.start()