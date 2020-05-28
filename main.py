from dataset.CsvReader import Reader
from algorithm.CalculateScore import *


def csv_write(file_name, result):
    csv_file = open(file_name, "w")
    
    # header
    csv_file.write("Rate, Score-1, Score-2\n")

    for entry in result:
        entry_to_string = ", ".join([str(e) for e in entry])
        csv_file.write(entry_to_string + "\n")
    csv_file.close()


def main():
    # open corpus
    reader = Reader()
    lines = reader.open_csv(1, 0)

    # result
    result = []
    accuracy_naive = 0
    accuracy_neg = 0

    for line in lines:
        review = line[0]
        answer = float(line[1])

        # calculate score
        score_naive = get_score(review, ['sent'])
        score_neg = get_score(review, ['neg'])
        print("score_naive: %7.2f, score_neg: %7.2f, answer: %5.2f" % (score_naive, score_neg, answer))

        # add difference with answer
        accuracy_naive += abs(score_naive - answer)
        accuracy_neg += abs(score_neg - answer)
        result.append([answer, score_naive, score_neg])

    # print overall accuracy
    print("accuracy_naive: %6.3f, accuracy_neg: %6.3f" % (accuracy_naive / len(lines), accuracy_neg / len(lines)))

    # save
    csv_write("scoring_result.csv", result)


if __name__ == "__main__":
    main()
