import os


txt = input("Name of txt file: ")


cur = os.path.dirname(os.path.abspath(__file__))


f = open(cur + '/' + txt, 'rt', encoding='UTF8')

comments = []

while True:
    line = f.readline()
    if not line: break
    line = eval(line)
    comments.append(line["text"])

f.close()

print(comments[0:10])