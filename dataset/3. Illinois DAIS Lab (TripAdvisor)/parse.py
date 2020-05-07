import os
import csv

def save(output,dirname):
	print(dirname,len(output))
	fullname = os.path.join(dirname,'output('+str(len(output))+').csv')
	f = open(fullname,'w',newline='')
	wr = csv.writer(f)
	wr.writerow(output)
	f.close()

def ReadnSave(names,dirname):
	output = []
	for name in names:
		f = open(name,'r')
		for i in range(3): 	line = f.readline() #앞에 3줄 무시
		while line:
			if  "<Content>" in line:
				review = line[9:]
				line = f.readline()
				while line:
					if "<Overall>" in line:
						rate = float(line[-2])
						output.append((review,rate))
						break
					line = f.readline()
			line = f.readline()
		f.close()
	save(output,dirname)

def search(dirname):
	filenames = os.listdir(dirname)
	non_parse = []
	for filename in filenames:
		full_filename = os.path.join(dirname,filename)
		ext = os.path.splitext(full_filename)[-1]
		if ext == '.dat': ##Diff for every Dataset
			non_parse.append(full_filename)
	ReadnSave(non_parse,dirname)


search(os.getcwd())

