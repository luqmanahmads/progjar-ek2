import threading
import socket
import sys
import time
import string
from multiprocessing import Process, Lock


#inisialisasi
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print >>sys.stderr, "Creating TCP socket succfessful..."

#binding socket to address:port
server_address = ('localhost', 11004)
print >>sys.stderr, "Binding to %s port %s successful..." % server_address
sock.bind(server_address)

#listening
sock.listen(1)

#commandlist
listCommand = ['login', 'register', 'exit', 'whoami', 'online', 'send', 'broadcast', 'chatgroup', 'joingroup', 'creategroup','logout', 'check', 'checkall']

#global variable all user
username = []
userpass = []
userindex = []
useraddr = []
usersock = []

#gobal variable all group
groupname = []
grouppass = []
groupmember = []

#fungsi untuk memperbarui userindex
def renew(index):
    for i in range(len(userindex)):
        if userindex[i]>index:
            userindex[i] = userindex[i] - 1

#fungsi untuk logout
def logout(client_username):
    if client_username in username:
        index = username.index(client_username)
        sock_index = userindex[index]
        del useraddr[sock_index]
        del usersock[sock_index]
        userindex[index] = -1
        renew(sock_index)        
        print "online : ", useraddr        
        print "user status : ", userindex        
        return "SUKSES : logged out\n"
    else:
        return "GAGAL\n"

#fungsi untuk login user
def login(client_username, client_password, koneksi_client, alamat_client):
    if client_username in username:
        index = username.index(client_username)        
        if userindex[index]==-1:
            if client_password == userpass[index]:
                useraddr.append(alamat_client)
                usersock.append(koneksi_client)
                sock_index = len(usersock) - 1
                userindex[index] = sock_index
                
                print "online : ", useraddr
                print "user status : ", userindex
                return "SUKSES : login berhasil\n"                
            else:
                return "GAGAL : password salah\n"
        else:
            return "GAGAL : anda sudah login\n"
    else:
        return "GAGAL : username tidak ditemukan\n"

#fungsi untuk register user
def register(reg_username, reg_password, reg_retype_password):
    if reg_username in username:
        return "GAGAL : username sudah terpakai\n"
    else:
        if reg_password == reg_retype_password:
            f = open("db.txt", "a")
            f.write(reg_username+"\n")
            f.write(reg_password+"\n")
            f.close()
            
            username.append(reg_username)
            userpass.append(reg_password)
            userindex.append(-1)
            
            return "SUKSES : berhasil membuat akun"
        else:
            return "GAGAL : password tidak cocok"

#fungsi auntentikasi
def authenticate(alamat_client):
    for item in useraddr:
        if item[0] == alamat_client[0] and item[1] == alamat_client[1]:
            return 1
    return 0

#fungsi untuk mengirim pesan private
def kirim(username_pengirim, username_penerima, pesan):
    if username_penerima in username:
        index = username.index(username_penerima)
        sock_index = userindex[index]    
        if sock_index > -1:
            usersock[sock_index].send("["+username_pengirim+"] "+pesan+"\n")
            return "SUKSES : pesan terkirim\n"
        else:
            return "GAGAL : penerima tidak online\n"
    else:
        return "GAGAL : username penerima belum terdaftar\n"
        
#fungsi untuk mengirim pesan broadcast
def broadcast(username_pengirim, pesan):
    for i in range(len(usersock)):
        usersock[i].send("[broadcast:"+username_pengirim+"] "+pesan+"\n")
    return "SUKSES : pesan terkirim\n"

#fungsi untuk mengirim pesan ke group
def chatgroup(username_pengirim, group_penerima, pesan):
    if group_penerima in groupname:
        indexGroup = groupname.index(group_penerima)
        if username_pengirim in groupmember[indexGroup]:
            for user in groupmember[indexGroup]:
                indexUser = username.index(user)
                indexSock = userindex[indexUser]
                if indexSock > -1:
                    usersock[indexSock].send("["+group_penerima+":"+username_pengirim+"] "+pesan+"\n")
            return "SUKSES : pesan terkirim\n"
        else:
            return "GAGAL : anda bukan anggota group\n"
    else:
        return "GAGAL : nama group tidak terdaftar\n"

#fungsi untuk bergabung dengan group
def joingroup(client_username, group, password):
    if group in groupname:
        indexGroup = groupname.index(group)       
        if password == grouppass[indexGroup]:
            if client_username in groupmember[indexGroup]:
                return "GAGAL : anda sudah menjadi bagian dari grup\n"
            else:
                groupmember[indexGroup].append(client_username)
                f = open("db_group.txt", "w")
                for i in range(len(groupname)):
                    f.write(groupname[i]+"\n")
                    f.write(grouppass[i]+"\n")
                    for j in range(len(groupmember[i])):
                        f.write(groupmember[i][j]+"\n")
                    f.write("*\n")
                f.close()
                return "SUKSES : bergabung ke grup\n"
        else:
            return "GAGAL : password group salah\n"
    else:
        return "GAGAL : grup tidak ada\n"

def creategroup(group, password):
    if group in groupname:
        return "GAGAL : nama group sudah terpakai\n"        
    else:
        groupname.append(group)
        grouppass.append(password)
        groupmember.append([])
        
        f = open("db_group.txt", "w")
        for i in range(len(groupname)):
            f.write(groupname[i]+"\n")
            f.write(grouppass[i]+"\n")
            for j in range(len(groupmember[i])):
                f.write(groupmember[i][j]+"\n")
            f.write("*\n")
        f.close()
        return "SUKSES : membuat group\n"

#fungsi untuk inisialisasi : loading user, dll
def initialize():
    print "loading user list.."
    counter = 0
    with open("db.txt") as f:
        for line in f:
            line = line.strip()
            if counter % 2 == 0:
                username.append(line)
            else:
                userpass.append(line)
                userindex.append(-1)
            counter = counter + 1
    
    f.close()
    return 1
    
def initializeGroup():
    print "loading group list.."
    counter = 0
    with open("db_group.txt") as f:
        for line in f:
            line = line.strip()
            if counter == 0:
                groupname.append(line)
                indexGroup = len(groupname) - 1
                newList = []
                counter = counter + 1
            elif counter == 1:
                grouppass.append(line)
                counter = counter + 1
            elif line in ['*']:
                groupmember.append(newList)
                counter = 0
            else:
                newList.append(line)
                counter = counter + 1
    f.close()
    return 1              

#fungsi untuk melayani servis client
def service(koneksi_client, alamat_client):
    try:
        #print >>sys.stderr, "ada koneksi dari client", alamat_client
        sys.stdout.flush()
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
                elif command[0] in ['register']:
                    if len(command) == 4:
                        message = register(command[1], command[2], command[3])
                    else:
                        message = "GAGAL : syntax error\n"    
                    
                elif command[0] in ['exit']:
                    break
                else:
                    if command[0] in ['logout', 'send', 'online', 'whoami', 'broadcast', 'chatgroup', 'joingroup', 'creategroup']:
                        if authenticate(alamat_client) == 1:
                            if command[0] in ['send']:
                                if len(command) > 2:
                                    pesan = ""                                    
                                    for i in range(len(command)):
                                        if i >= 2:
                                            pesan = pesan + command[i] + " "
                                    message = kirim(client_username, command[1], pesan)
                                else:
                                    message = "GAGAL : penggunaan [send] [user_pengirim] [pesan]\n"
                            if command[0] in ['online']:
                                if len(command) == 1:
                                    for i in range(len(userindex)):
                                        if userindex[i] > -1:
                                            koneksi_client.send(username[i]+"\n")
                                    message = "SUKSES\n"
                            if command[0] in ['whoami']:
                                koneksi_client.send("login as : "+client_username+"\n")
                                koneksi_client.send("address : "+alamat_client[0]+"\n")
                                koneksi_client.send("port : "+str(alamat_client[1])+"\n")
                                message = "SUKSES\n"
                            
                            if command[0] in ['broadcast']:
                                if len(command) > 1:
                                    pesan = ""                                    
                                    for i in range(len(command)):
                                        if i >= 1:
                                            pesan = pesan + command[i] + " "
                                    message = broadcast(client_username, pesan)
                                else:
                                    message = "GAGAL : syntax error\n"
                                    
                            if command[0] in ['chatgroup']:
                                if len(command) > 2:
                                    pesan = ""
                                    for i in range(len(command)):
                                        if i >=2:
                                            pesan = pesan + command[i] + " "
                                message = chatgroup(client_username, command[1], pesan)
                            if command[0] in ['joingroup']:
                                if len(command) == 3:
                                    message = joingroup(client_username, command[1], command[2])
                                else:
                                    message = "GAGAL : syntax error\n"
                            
                            if command[0] in ['creategroup']:
                                if len(command) == 3:
                                    message = creategroup(command[1], command[2])
                                else:
                                    message = "GAGAL : syntax error\n"
                            if command[0] in ['logout']:
                                if len(command) == 1:
                                    message = logout(client_username)
                                else:
                                    message = "GAGAL : syntax error\n"
                        else:
                            message = "GAGAL : anda tidak terautentikasi\n"
                    else:
                        message = "GAGAL : command error\n"
            else:
                message = "GAGAL : command tidak tersedia\n"
            koneksi_client.send(message)
    finally:
        koneksi_client.close()

#load user information
initialize()
print "user list : ", username
#print userpass
print "user status : ", userindex

#load group info
initializeGroup()
print "group list : ", groupname
#print grouppass 
#print groupmember[0]
#print groupmember[1]

print "\n==============================="
print "WELCOME TO MULTICHAT SERVER EK2"
print "==============================="

#main service
while True:
    print >>sys.stderr, "waiting for connection"
    sys.stdout.flush()
    koneksi_client, alamat_client = sock.accept()
    
    s = threading.Thread(target=service, args=(koneksi_client, alamat_client))
    s.start()