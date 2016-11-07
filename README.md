[PROTOKOL CHAT SERVER]
======================

SIGN UP
=======
- Format message :
	SIGNUP spasi USERNAME spasi PASSWORD
- Parameter
	- username: alphanumerik (tanpa spasi)
	- password: alphanumerik (tanpa spasi)
- Return
	- Request berhasil diproses: [OK] sign up berhasil
	- Request gagal diproses :
		- Username sudah terpakai :
			[ERR] Username sudah terpakai
		- Format message sign up tidak sesuai :
			[ERR] Format message tidak sesuai

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
		- Username belum tersedia : 
    			[ERR] Username belum tersedia
		- Format message login tidak sesuai : 
    			[ERR] Format message tidak sesuai
		- Password yang dimasukkan salah : 
    			[ERR] Password yang dimasukkan salah
			
LOGOUT
======
- Format message :
	LOGOUT
- Return
	- [OK] Logout berhasil

PRIVATE MESSAGE
===============
- Format message : 
	SEND spasi USERNAME_PENERIMA spasi MESSAGE
- Parameter
	- username penerima : alphanumerik (tanpa spasi)
	- message
- Return
	- Request berhasil diproses: [OK] pesan terkirim
	- Request gagal diproses :
		- Username penerima tidak tersedia atau belum terhubung dengan server : 
			[ERR] penerima tidak tersedia
		- Format message private message tidak sesuai : 
			[ERR] format message tidak sesuai

MEMBUAT GRUP
===========
- Format message :
	CREATEGROUP spasi NAMA_GRUP spasi PASSWORD_GRUP
- Parameter
	- nama grup : alphanumerik (tanpa spasi)
	- password: alphanumerik (tanpa spasi)
- Return
	- Request berhasil diproses: 
		[OK] Grup berhasil dibuat 
	- Request gagal diproses:
		- Nama grup sudah terpakai:
			[ERR] Nama grup sudah terpakai
		- Format message tidak sesuai
			[ERR] Format message tidak sesuai

JOIN GRUP
=========
- Format message : 
	JOIN spasi NAMA_GRUP spasi PASSWORD_GRUP
- Parameter
	- nama grup : alphanumerik (tanpa spasi)
	- password: alphanumerik (tanpa spasi)
- Return
	- Request berhasil diproses: [OK] Join grup berhasil
	- Request gagal diproses:
		- Ketika sudah menjadi anggota grup : 
			[ERR] Anda telah bergabung dalam grup
  		- Format message tidak sesuai : 
			[ERR] Format message tidak sesuai
  		- Nama grup tidak tersedia : 
		 	[ERR] Grup tidak tersedia
		- Password grup tidak sesuai : 
			[ERR] Password grup salah
			
MENGIRIM PESAN KE GRUP
=====================
- Format message
	 spasi NAMA_GROUP spasi MESSAGE
- Parameter
	- nama grup : alphanumerik (tanpa spasi)
	- message
- Return
	- Request berhasil diproses: [OK] Pesan terkirim
	- Request gagal diproses:
		- Nama grup tidak tersedia:
			[ERR] Nama grup tidak tersedia
		- Format message tidak sesuai:
			[ERR] Format message tidak sesuai
		- Pengirim belum tergabung dalam grup:
			[ERR] Anda belum bergabung dalam grup

KELUAR DARI GRUP
================
- Format message :
	LEAVE spasi NAMA_GROUP
- Parameter
	- nama grup : alphanumerik (tanpa spasi)
- Return
	- Request berhasil diproses: [OK] Berhasil keluar dari grup
	- Request gagal diproses:
		- Nama grup tidak tersedia : 
			[ERR] Nama grup tidak tersedia
		- Format message tidak sesuai :
			[ERR] Format message tidak sesuai
		- Belum tergabung dalam grup : 
			[ERR] Anda belum bergabung dalam grup


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

