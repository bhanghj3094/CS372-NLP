import os
import csv

def save(output,dirname):
	fullname = os.path.join(dirname,'output('+str(len(output))+')csv')
	f = open(fullname,'w',newline='')
	wr = csv.writer(f)
	wr.writerow(output)
	f.close()

def ReadnSave(ratings,reviews,dirname):
	output = []
	f_rating = open(os.path.join(dirname,ratings),'r')
	f_review = open(os.path.join(dirname,reviews), 'r')
	rat = f_rating.readline()
	rev = f_review.readline()
	while rat :
		output.append((rev,(float(rat)*5)))
		rat = f_rating.readline()
		rev = f_review.readline()
	f_rating.close()
	f_review.close()
	save(output,dirname)

def search(dirname):
	filenames = os.listdir(dirname)
	for filename in filenames:
		full_filename = os.path.join(dirname,filename)
		ext = os.path.split(full_filename)[-1]
		if "rating" in ext: ##Diff for every Dataset
			rating_dir = ext
		elif "subj" in ext:
			review_dir = ext
	ReadnSave(rating_dir,review_dir,dirname)

def explore_categories(dirname):
	categories = os.listdir(dirname)
	for cate in categories:
		fullname = os.path.join(dirname,cate)
		if os.path.isdir(fullname):
			search(cate)

explore_categories(os.getcwd())

