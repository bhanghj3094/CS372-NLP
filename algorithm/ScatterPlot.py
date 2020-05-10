import matplotlib.pyplot as plt
import numpy as np
import csv

rate = list()
score = list()

# rate = np.random.randint(1, 6, 20)
# score = np.random.randint(0, 20, 20)

f = open('scoring_result.csv', 'r', encoding='utf-8')
reader = csv.reader(f)
for line in reader:
    temp = line.split(",")
    rate.append(int(temp[0]))
    score.append(float(temp[1]))
f.close()

scatter = plt.scatter(rate, score, color='black')

plt.xlim(0, 6)
plt.ylim(np.min(score-1), np.max(score+1))

plt.title('ScatterPlot of Rate and Review Score', pad=10)
plt.xlabel('Rate', labelpad=10)
plt.ylabel('Review Score', labelpad=10)

plt.show()