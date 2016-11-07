[PROTOKOL CHAT SERVER]
======================

LOGIN
========
- Format message : 
	LOGIN spasi USERNAME spasi PASSWORD
- Parameter
	- username: alphanumerik (tanpa spasi)
	- password: alphanumerik (tanpa spasi)
- Return
  - Request berhasil diproses: [OK] login berhasil
  - Request gagal diproses :
    - Username belum tersedia : [ERR] Username belum tersedia
    - Format message login tidak sesuai : [ERR] Format message tidak sesuai
    - Password yang dimasukkan salah : [ERR] Password yang dimasukkan salah



[PROTOKOL FTP SERVER]
=====================

AUTHENTICATION :
================
USER [username] -> untuk memasukkan username
PASS [password] -> untuk memasukkan password

REQUEST :
=========
LIST 			-> untuk melihat daftar file pada direktori
RETR [nama_file]	-> untuk mendownload file bernama nama_file
CD [nama_direktori]	-> untuk pindah direktori ke nama_direktori
PUT [nama_file]		-> untuk upload file bernama nama_file
DEL [nama_file]		-> untuk menghapus file di server
EXIT			-> untuk menutup koneksi denggan server

RESPONSE :
==========
[OK] [message]	-> request berhasil di proses
[ERR] [message]	-> request gagal di proses


[PROTOKOL CHAT SERVER]
==============
