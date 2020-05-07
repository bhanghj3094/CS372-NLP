import os
import csv

class Reader():
	def __init__(self):
		self.directory = os.getcwd() #code directory, 기본 설정 :  가장 바깥으로
		self.folder = ''
		self.file = ''

	def get_folder(self,num):
		
		folders = os.listdir(self.directory)
		dirs = []
		for fold in folders:
			if os.path.isdir(os.path.join(self.directory,fold)):
				dirs.append(fold)
		dirs = sorted(dirs)
		print(dirs)
		return os.path.join(self.directory,dirs[num-1]) #Folder number starts from 1 (1~5)

	def get_file(self,folder,num):
		files = os.listdir(folder)
		files = sorted(files)
		return os.path.join(folder,files[num]) #File num starts from 0

	def open_csv(self,folder,file): #Return (Review_text,Rating) Tuple List
		tuples = []
		self.folder = self.get_folder(folder)
		self.file =  self.get_file(self.folder,file)
		f = open(self.file,'r',encoding='utf-8')
		rdr = csv.reader(f)
		for line in rdr:
			tuples.append(line)
		f.close()
		return tuples

class InteractiveReader(Reader): 

	def __init__(self):
		self.directory = os.getcwd()
		self.folder = ''
		self.file = ''

		n = input('\n\npress y to continue : ')
		while n =='y':
			tuples = []
			self.folder = self.get_folder(int(input("Choose folder number(1~5) : ")))
			self.file = self.get_file(self.folder,int(input("Choose file number(1~) : ")))
			f = open(self.file,'r',encoding='utf-8')
			rdr = csv.reader(f)
			for line in rdr:
				tuples.append(line)
			f.close()
			print(tuples)
			n = input('\n\npress y to continue : ')
"""
1. Datasets 폴터 가장 상단에 놓고 사용 
2. 폴더번호는 1번, 파일번호는 0번 부터 시작

#csvReader Usage
rdr = Reader()
print(rdr.open_csv(3,1))

#interactiveReader() Usage
rdr = InteractiveReader()
"""