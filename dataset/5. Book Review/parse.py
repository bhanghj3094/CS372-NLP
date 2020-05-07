import os
import csv

def save(output,dirname):
	print(dirname,len(output))
	fullname = os.path.join(dirname,'output.csv')
	f = open(fullname,'w',newline='')
	wr = csv.writer(f)
	wr.writerow(output)
	f.close()

def ReadnSave(names,dirname):
	output = []
	for name in names:
		f = open(name,'r')
		line = f.readline()
		while line:
			if line == "<rating>\n":
				rate = float(f.readline())
				while True:
					review = f.readline()
					if review == "<review_text>\n":
						review = f.readline()
						output.append((review,rate))
						break
			line = f.readline()
		f.close()
	save(output,dirname)

def search(dirname):
	filenames = os.listdir(dirname)
	non_parse = []
	for filename in filenames:
		full_filename = os.path.join(dirname,filename)
		if os.path.isdir(full_filename):
			search(full_filename)
		else:
			ext = os.path.splitext(full_filename)[-1]
			if ext == '.review': ##Diff for every Dataset
				non_parse.append(full_filename)
	ReadnSave(non_parse,dirname)

def explore_categories(dirname):
	categories = os.listdir(dirname)
	for cate in categories:
		fullname = os.path.join(dirname,cate)
		if os.path.isdir(fullname):
			search(cate)

explore_categories(os.getcwd())

