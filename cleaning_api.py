from flask import Flask, render_template, request
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory
from bahasa.stemmer import Stemmer
from werkzeug.utils import secure_filename
import json, nltk, os, csv, re, string
import pandas as pd

server = Flask(__name__)



@server.route("/Input-Text", methods=['POST','GET'])
def InputText():
	#Fungsi Untuk Menampilkannya Input Text Ke Dalam Api
	if request.method == "GET":
		return render_template('input-text.html')
	
	elif request.method == "POST":
		data = request.form['kirim']
		api = Text_to_API(data)
		return api

def Text_to_API(text):
	data = {"data":text}
	return data



@server.route("/Upload-File", methods=['POST','GET'])
def BukaFile():
	#Fungsi Untuk Membuka File & Menampilkannya Dalam API
	if request.method == "GET":
		return render_template('buka-file.html')
	
	elif request.method == "POST":
		file = request.files['upload_file'] #untuk mengambil file yang diinput oleh user
		filename = secure_filename(file.filename) #untuk mengambil nama file yang di input user
		file.save(f"File User/{filename}") #Untuk menyimpan File Dalam Folder
		api = BacaFile(f"File User/{filename}")
		return api

def BacaFile(path):
	#Fungsi Untuk Membaca File
	with open(path, 'r') as dataku:
		reader = csv.reader(dataku, delimiter=',')
		data = pd.DataFrame(list(reader))
	
	hasil = {"data":data.values.tolist()} #Biar Bisa Jadi JSON, Kolom Harus Dijadikan List
	return hasil



@server.route("/TokenizeText", methods=['POST','GET'])
def TokenizeText():
	#Fungsi Untuk Melakukan Tokenize Dalam Text & Menampilkannya Dalam Api
	if request.method == "GET":
		return render_template("tokenise-text.html")
	
	elif request.method == "POST":
		data = request.form['token']
		api = Token(data)
		return api
		
def Token(text): #Fungsi Untuk Tokenize Input Text Ke Dalam API
	tokens = nltk.tokenize.word_tokenize(text)
	hasil = tokens
	data = {"data":hasil}
	return data



@server.route("/TokenizeFile", methods=['POST','GET'])
def TokenizeFile():
	#Fungsi Untuk Melakukan Tokenize Dalam File & Menampilkannya Dalam Api
	if request.method == "GET":
		return render_template('upload-file-tokenize.html')
	elif request.method == "POST":
		file = request.files['upload_file'] #untuk mengambil file yang diinput oleh user
		filename = secure_filename(file.filename) #untuk mengambil nama file yang di input user
		file.save(f"File User/{filename}") #Untuk menyimpan File Dalam Folder
		api = Upload_File_Token(f"File User/{filename}")
		return api
		
def Upload_File_Token(path): #Fungsi Untuk Tokenize File Ke Dalam Api
	with open(path, 'r') as dataku:
		reader = csv.reader(dataku, delimiter=',')
		data = pd.DataFrame(list(reader))
	
	hasil = []      # Penyimpanan data tokenize dari tweet kolom 0
	for i in data[0][:51]:
		tokens = nltk.tokenize.word_tokenize(i)
		hasil.append(tokens)
	
	temp = {"data":hasil}
	return temp



@server.route('/LowerText', methods=['POST','GET'])
def LowerText():
	#Fungsi Untuk Melakukan LowerText Dalam Text & Menampilkannya Dalam Api
	if request.method == "GET":
		return render_template('lower-text.html')
	
	elif request.method == "POST":
		data = request.form['lower']
		api = ProsesLower(data)
		return api

def ProsesLower(text): # Fungsi Untuk Melower Text
	hasil = text.lower()
	data = {"data":hasil}
	return data



@server.route('/LowerFile', methods=['POST','GET'])
def LowerFile():
	#Fungsi Untuk Melakukan LowerText Dalam File & Menampilkannya Dalam Api
	if request.method == "GET":
		return render_template('upload-file-lower.html')
	
	elif request.method == "POST":	
		file = request.files['upload_lower_file'] #untuk mengambil file yang diinput oleh user
		filename = secure_filename(file.filename) #untuk mengambil nama file yang di input user
		file.save(f"File User/{filename}") #Untuk menyimpan File Dalam Folder
		api = File_Lower(f"File User/{filename}")
		return api
	
def File_Lower(path): #Fungsi Untuk Lower File
	with open(path, 'r') as dataku:
		reader = csv.reader(dataku, delimiter=',')
		data = pd.DataFrame(list(reader))
	
	hasil = [] 
	for i in data[0][:51]:
		text = i.lower()
		hasil.append(text)
	
	temp = {"data":hasil}
	return temp



@server.route('/Normalisasi-Text', methods=['POST','GET'])
def Normalisasi():
	#Fungsi Untuk Melakukan Normalisasi Text
	if request.method == "GET":
		return render_template('normalisasi-text.html')
	elif request.method == "POST":
		data = request.form['normalisasi']
		file = request.files['kamusalay'] #untuk mengambil file yang diinput oleh user
		filename = secure_filename(file.filename) #untuk mengambil nama file yang di input user
		file.save(f"File User/{filename}") #Untuk menyimpan File Dalam Folder
		api = Text_Normalisasi(data, f"File User/{filename}")
		return api
		
def Text_Normalisasi(text, path):	#Fungsi Untuk Normalisasi Text
	with open(path, 'r') as dataku:
		reader = csv.reader(dataku, delimiter=',')
		data = pd.DataFrame(list(reader))
	
	normalisasi = []
	text_list = text.split(" ")
	for i in text_list:
		if i in data[0].tolist():
			no = data[0].tolist().index(i)
			text = text.replace(i, data[1][no])
	
	hasil = {"data":text}
	return hasil
	



@server.route('/Normalisasi-File', methods=['POST','GET'])
def Normalisasi_File():
	if request.method == "GET":
		return render_template("upload-file-normalisasi.html")
	elif request.method == "POST":
		file = request.files['kamus_alay'] #untuk mengambil file yang mau dinormalisasi oleh user
		user_file = secure_filename(file.filename) #untuk mengambil nama file yang di input user
		file.save(f"File User/{user_file}") #Untuk menyimpan File Dalam Folder
		
		file = request.files['kamusalay'] #untuk mengambil file kamus yang diinput oleh user
		kamus = secure_filename(file.filename) #untuk mengambil nama file yang di input user
		file.save(f"File User/{kamus}") #Untuk menyimpan File Dalam Folder
		
		api = File_Normalisasi(f"File User/{user_file}", f"File User/{kamus}")
		return api

def File_Normalisasi(user_file, kamus):
	with open(user_file, 'r') as dataku:
		reader = csv.reader(dataku, delimiter=',')
		data = pd.DataFrame(list(reader))
	
	with open(kamus, 'r') as dataku:
		reader = csv.reader(dataku, delimiter=',')
		data1 = pd.DataFrame(list(reader))
	
	normalisasi = []
	for kalimat in data[0][:51]:
		kalimat_list = kalimat.split(" ")
		for i in kalimat_list:
			if i in data1[0].tolist():
				no = data1[0].tolist().index(i)
				kalimat = kalimat.replace(i, data1[1][no])
		normalisasi.append(kalimat)
	
	hasil = {"data":normalisasi}
	return hasil


@server.route('/SteammingText', methods=['POST','GET'])
def SteammingText():
	#Fungsi Untuk Melakukan Steamming Text & Menampilkannya Dalam Api
	if request.method == "GET":
		return render_template('steaming-text.html')
	elif request.method == "POST":
		data = request.form['steaming']
		api = Text_Steaming(data)
		return api

def Text_Steaming(text):
	hasil_stemming = []
	stemmer = Stemmer()
	hasil = stemmer.stem(text)
	hasil_stemming.append(hasil)
	data = {"data":hasil_stemming}
	return data



@server.route('/SteammingFile', methods=['POST','GET'])
def SteammingFile():
	#Fungsi Untuk Melakukan Steamming File & Menampilkannya Dalam Api
	if request.method == 'GET':
		return render_template('upload-file-steaming.html')
	elif request.method == "POST":
		file = request.files['upload_steaming_file'] #untuk mengambil file yang diinput oleh user
		filename = secure_filename(file.filename) #untuk mengambil nama file yang di input user
		file.save(f"File User/{filename}") #Untuk menyimpan File Dalam Folder
		api = File_Steaming(f"File User/{filename}")
		return api

def File_Steaming(path):
	with open(path, 'r') as dataku:
		reader = csv.reader(dataku, delimiter=',')
		data = pd.DataFrame(list(reader))
	hasil_stemming = []

	for i in data[0][:51]:
		stemmer = Stemmer()
		hasil = stemmer.stem(i)
		hasil_stemming.append(hasil)
	temp = {"data":hasil_stemming}
	return temp

@server.route('/StopwordText', methods=['POST','GET'])
def StopwordText():
	#Fungsi Untuk Melakukan Stopword Dari Input Text & Menampilkannya Dalam Api
	if request.method == "GET":
		return render_template('stopword-text.html')
	elif request.method == "POST":
		data = request.form['stopword']
		api = Text_Stopword(data)
		return api

def Text_Stopword(text):
	factory = StopWordRemoverFactory()
	stopword = factory.create_stop_word_remover()

	hasil={'data':[]}
	hasil['data'].append(stopword.remove(text))
	return hasil



@server.route('/StopwordFile', methods=['POST','GET'])
def StopwordFile():
	#Fungsi Untuk Melakukan Stopword Dari File & Menampilkannya Dalam Api
	if request.method == "GET":
		return render_template('upload-file-stopword.html')
	elif request.method == "POST":
		file = request.files['upload_stopword_file'] #untuk mengambil file yang diinput oleh user
		filename = secure_filename(file.filename) #untuk mengambil nama file yang di input user
		file.save(f"File User/{filename}") #Untuk menyimpan File Dalam Folder
		api = File_Stopword(f"File User/{filename}")
		return api

def File_Stopword(path):
	with open(path, 'r') as dataku:
		reader = csv.reader(dataku, delimiter=',')
		data = pd.DataFrame(list(reader))
	
	factory = StopWordRemoverFactory()
	stopword = factory.create_stop_word_remover()

	hasil={'data':[]}
	for i in data[0][:51]:
		kalimat1 =i
		hasil['data'].append(stopword.remove(kalimat1))
	
	return hasil



@server.route('/Karakter-Text', methods=['POST','GET'])
def Karakter():
	if request.method == "GET":
		return render_template('karakter-text.html')
	elif request.method == "POST":
		data = request.form['karakter']
		api = Hapus_Karakter(data)
		return api

def Hapus_Karakter(text):
	hasil = ""
	izin = [' ','=','>','<']
	for i in text:
		if i.isalpha() or i.isnumeric() or i in izin:
			hasil = hasil + i
	hasil = hasil.replace('\\t'," ").replace('\\n'," ").replace('\\u'," ").replace('\\',"")
	# remove non ASCII (emoticon, chinese word, .etc)
	hasil = hasil.encode('ascii', 'replace').decode('ascii')
	# remove mention, link, hashtag
	hasil = ' '.join(re.sub("([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)"," ", hasil).split())
	#remove punctuation
	hasil = hasil.translate(str.maketrans("","",string.punctuation))
	#remove whitespace leading & trailing
	hasil = hasil.strip()
	# remove single char
	hasil = re.sub(r"\b[a-zA-Z]\b", "", hasil)
	#remove multiple whitespace into single whitespace
	hasil = re.sub('\s+',' ',hasil)
	hasil = re.sub('\S*\d\S*\s*','',hasil).strip()
	hasil = re.sub('\[.*\]','',hasil).strip()
	# remove stock market tickers like $GE
	hasil = re.sub(r'\$\w*', '', hasil)
	hasil = re.sub(r'^rt[\s]+','', hasil)
	hasil = re.sub(r'^RT[\s]+','', hasil)
	hasil = re.sub(r'#', '', hasil)
	# remove hyperlinks
	hasil = re.sub(r'https?:\/\/.[\r\n]', '', hasil)
	hasil = re.sub(r',','.',hasil)
	# remove incomplete URL
	hasil = hasil.replace("http://", " ").replace("https://", " ")
	data = {"data":hasil}
	return data



@server.route('/Karakter-File', methods=['POST','GET'])
def File_Karakter():
	if request.method == "GET":
		return render_template('upload-karakter-file.html')
	elif request.method == "POST":
		file = request.files['upload_karakter_file'] #untuk mengambil file yang diinput oleh user
		filename = secure_filename(file.filename) #untuk mengambil nama file yang di input user
		file.save(f"File User/{filename}") #Untuk menyimpan File Dalam Folder
		api = Karakter_File(f"File User/{filename}")
		return api

def Karakter_File(path):
	with open(path, 'r') as dataku:
		reader = csv.reader(dataku, delimiter=',')
		data = pd.DataFrame(list(reader))
	
	akhir = []
	for a in data[0][:51]:
		hasil = ""
		izin = [' ','=','>','<']
		for i in a:
			if i.isalpha() or i.isnumeric() or i in izin:
				hasil = hasil + i
		hasil = hasil.replace('\\t'," ").replace('\\n'," ").replace('\\u'," ").replace('\\',"")
		# remove non ASCII (emoticon, chinese word, .etc)
		hasil = hasil.encode('ascii', 'replace').decode('ascii')
		# remove mention, link, hashtag
		hasil = ' '.join(re.sub("([@#][A-Za-z0-9]+)|(\w+:\/\/\S+)"," ", hasil).split())
		#remove punctuation
		hasil = hasil.translate(str.maketrans("","",string.punctuation))
		#remove whitespace leading & trailing
		hasil = hasil.strip()
		# remove single char
		hasil = re.sub(r"\b[a-zA-Z]\b", "", hasil)
		#remove multiple whitespace into single whitespace
		hasil = re.sub('\s+',' ',hasil)
		hasil = re.sub('\S*\d\S*\s*','',hasil).strip()
		hasil = re.sub('\[.*\]','',hasil).strip()
		# remove stock market tickers like $GE
		hasil = re.sub(r'\$\w*', '', hasil)
		hasil = re.sub(r'^rt[\s]+','', hasil)
		hasil = re.sub(r'^RT[\s]+','', hasil)
		hasil = re.sub(r'#', '', hasil)
		# remove hyperlinks
		hasil = re.sub(r'https?:\/\/.[\r\n]', '', hasil)
		hasil = re.sub(r',','.',hasil)
		# remove incomplete URL
		hasil = hasil.replace("http://", " ").replace("https://", " ")
		akhir.append(hasil)
	
	temp = {"data":akhir}
	return temp



if __name__ == "__main__":
	server.run(debug=True)