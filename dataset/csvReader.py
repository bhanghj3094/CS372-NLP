import os
import csv

class Reader():
	def __init__(self):
		self.directory = os.getcwd()
		self.folder = ''
		self.file = ''
	def get_folder(self,directory,num):
		
		folders = os.listdir(directory)
		folders = sorted(folders)

		return os.path.join(directory,folders[num])

	def get_file(self,directory,num):
		files = os.listdir(directory)
		files = sorted(files)

		return os.path.join(directory,files[num])

	def open_csv(self,folder,file):
		tuples = []
		self.folder = self.get_folder(self.directory,folder)
		self.file =  self.get_file(self.folder,file)
		f = open(self.file,'r',encoding='utf-8')
		rdr = csv.reader(f)
		for line in rdr:
			tuples.append(line)
		f.close()
		return tuples

rdr = Reader()
print(rdr.open_csv(5,1))