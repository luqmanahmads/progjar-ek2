DESKRIPSI UMUM
==============
Merupakan repositori kelompok 2 dalam mata kuliah Pemrograman Jaringan E Teknik Informatika ITS 2016/2017 untuk dipergunakan sebaik - baiknya

Repository ini terdiri dari :

1. Simple FTP server
2. Multichat Server Kelompok 2
3. GUI Client dari Chat Server Kelompok 3

PROTOKOL CHAT SERVER KELOMPOK 2
=================================

General Proses
---------------

1. Register
-----------
- Deskripsi :
	untuk membuat akun baru bagi user yang belum terdaftar.
- Format message :
	Register spasi USERNAME spasi PASSWORD spasi VALIDASI PASSWORD
- Parameter
	- username: alphanumerik (tanpa spasi)
	- password: alphanumerik (tanpa spasi)
- Return
	- Akun berhasil terdaftar: 100
	- Request gagal diproses :
		- Username sudah terpakai : 231
		- Password tidak cocok : 232

2. Login
---------
- Deskripsi :
	digunakan untuk mengautentifikasi akun yang sudah terdaftar pada chat server
- Format message : 
	LOGIN spasi USERNAME spasi PASSWORD
- Parameter
	- username: alphanumerik (tanpa spasi)
	- password: alphanumerik (tanpa spasi)
- Return
	- Request berhasil diproses: 100
	- Request gagal diproses :
		- Username belum tersedia : 241
		- Syntax error : 210 
		- Password yang dimasukkan salah : 232
		- Username yang dipakai sudah/sedang online : 243 

3. Exit
-------
- Deskripsi : 
	Digunakan untuk menutup socket dan memutuskan hubungan dengan server.
- Format message :
	Exit
- Return
	Sukses : 100


Process With Login
------------------

1. Private Message
------------------
- Deskripsi :
	untuk mengirim pesan pribadi pada user lain
- Format message : 
	SEND spasi USERNAME_PENERIMA spasi MESSAGE
- Parameter
	- username penerima : alphanumerik (tanpa spasi)
	- message
- Return
	- Request berhasil diproses: 100
	- Request gagal diproses :
		- Username penerima tidak terdaftar : 251 
		- Username penerima belum login : 220
		- Syntax error : 210
		
2. Check Our Self
-----------------
- Deskripsi :
	digunakan untuk mengecek username, alamat, port yang digunakan user untuk terhubung ke server
- Format message :
	Whoami
- Return
	- Request berhasil diproses :
		Status login berhasil : 100
	- Request gagal diproses :
		Belum login : 220
		
3. Check Online Friend
-----------------------
- Deskripsi :
	digunakan untuk mengecek user-user yang sedang terhubung ke server
- Format message :
	online
- Return :
	- Request berhasil diproses :
		List user yang sedang online : 100
	- Gagal :
		belum login : 220

4. Broadcast
-------------
- Deskripsi :
	digunakan untuk mengirim pesan ke semua user yang terdaftar di server
- Format message :
	broadcast spasi [isi_pesan]
- Return :
	Sukses : 100
	
5. Checkpast
-------------
- Deskripsi :
	digunakan untuk menampilkan seluruh pesan yang sudah terbaca
- Format message :
	checkpast
- Return :
	- Sukses : 100
	- Gagal :
		belum login : 220
		
6. Check
---------
- Deskripsi :
	untuk mengecek pesan yang masuk pada akun user
- Format message :
	check
- Return :
	
Membuat Group
-------------
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

Join Group
----------
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
			
Mengirim Pesan ke Group
-----------------------
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

Keluar dari Group
----------------
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


PROTOKOL FTP SERVER
===================

Authentication
--------------
USER [username] -> untuk memasukkan username
PASS [password] -> untuk memasukkan password

Request
-------
LIST 			-> untuk melihat daftar file pada direktori
RETR [nama_file]	-> untuk mendownload file bernama nama_file
CD [nama_direktori]	-> untuk pindah direktori ke nama_direktori
PUT [nama_file]		-> untuk upload file bernama nama_file
DEL [nama_file]		-> untuk menghapus file di server
EXIT			-> untuk menutup koneksi denggan server

Response
--------
[OK] [message]	-> request berhasil di proses
[ERR] [message]	-> request gagal di proses

