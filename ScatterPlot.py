import matplotlib.pyplot as plt
import numpy as np
import csv

rate = list()
score1 = list()
score2 = list()

# rate = np.random.randint(1, 6, 20)
# score = np.random.randint(0, 20, 20)

with open("scoring_result.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)  # skip header
    for row in reader:
        rate.append(float(row[0]))
        score1.append(float(row[1]))
        score2.append(float(row[2]))

plt.subplot(1, 2, 1)
scatter = plt.scatter(rate, score1, color="black", s=2)

plt.xlim(0, 6)
plt.ylim(np.min(score1) - 1, np.max(score1) + 1)

plt.title("ScatterPlot of Rate and Review Score(Naive Ver.)", pad=10)
plt.xlabel("Rate", labelpad=10)
plt.ylabel("Review Score", labelpad=10)

plt.subplot(1, 2, 2)
scatter = plt.scatter(rate, score2, color="black", s=2)

plt.xlim(0, 6)
plt.ylim(np.min(score2) - 1, np.max(score2) + 1)

plt.title("ScatterPlot of Rate and Review Score(Double Negation Ver.)", pad=10)
plt.xlabel("Rate", labelpad=10)
plt.ylabel("Review Score", labelpad=10)

plt.show()
