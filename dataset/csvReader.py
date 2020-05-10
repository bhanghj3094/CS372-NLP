import os
import csv
import pandas

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
		fo = os.path.join(self.directory,self.match_dir(dirs,num))
		return fo #Folder number starts from 1 (1~5)

	def match_dir(self,folders,num):
		for fold in folders:
			if fold[0] == str(num):
				return fold

	def get_file(self,folder,num):
		files = os.listdir(folder)
		files = sorted(files)
		return os.path.join(folder,files[num]) #File num starts from 0

	def open_csv(self,folder,file): #Return (Review_text,Rating) Tuple List
		self.folder = self.get_folder(folder)
		self.file =  self.get_file(self.folder,file)
		read_csv = pandas.read_csv(self.file,header=None).values.tolist()
		tuples = self.make_tuples(read_csv[0])
		return tuples

	def split(self,s):
		index = s.rfind(',')
		return (s[2:index-1],s[index+2:len(s)-1])

	def make_tuples(self,csv):
		tuples = []
		for tup in csv:
			tuples.append(self.split(tup))
		return tuples

"""
1. Datasets 폴터 가장 상단에 놓고 사용 
2. 폴더번호는 1번, 파일번호는 0번 부터 시작

#csvReader Usage
rdr = Reader()
print(rdr.open_csv(3,1))

"""

