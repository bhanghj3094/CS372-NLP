import os, csv
import pandas as pd


class Reader:
    """
	Dataset Reader for csv files. 
	Set working directory to current directory, and process read_csv.
	"""

    def __init__(self):
        self.directory = os.getcwd() + "/dataset"
        self.folder = ""
        self.file = ""

    def get_folder(self, num):
        folders = os.listdir(self.directory)
        dirs = []
        for fold in folders:
            if os.path.isdir(os.path.join(self.directory, fold)):
                dirs.append(fold)
        dirs = sorted(dirs)
        fo = os.path.join(self.directory, self.match_dir(dirs, num))
        return fo  # Folder number starts from 1 (1~5)

    def match_dir(self, folders, num):
        for fold in folders:
            if fold[0] == str(num):
                return fold

    def get_file(self, folder, num):
        files = os.listdir(folder)
        files = sorted(files)
        return os.path.join(folder, files[num])  # File num starts from 0

    # Return list of tuples [(Review_text, Rating), ..]
    def open_csv(self, folder, file):
        self.folder = self.get_folder(folder)
        self.file = self.get_file(self.folder, file)
        read_csv = pd.read_csv(self.file, header=None).values.tolist()
        tuples = self.make_tuples(read_csv[0])
        return tuples

    def split(self, s):
        index = s.rfind(",")
        return (s[2 : index - 1], s[index + 2 : len(s) - 1])

    def make_tuples(self, csv):
        tuples = []
        for tup in csv:
            tuples.append(self.split(tup))
        return tuples
