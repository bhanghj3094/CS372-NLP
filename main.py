from dataset.csvReader import Reader
from algorithm.CalculateScore import *


def open_youtube(file_name):
    f = open('dataset/Youtube Crawling/' + file_name, 'rt', encoding='UTF8')

    comments = []
    while True:
        line = f.readline()
        if not line: break
        line = eval(line)
        comments.append(line["text"])
    f.close()
    return comments


def csv_write(file_name, result):
    csv_file = open(file_name, "w")
    
    # header
    csv_file.write("Rate, Score-1, Score-2\n")

    for entry in result:
        entry_to_string = ", ".join([str(e) for e in entry])
        csv_file.write(entry_to_string + "\n")
    csv_file.close()


def main():
    # Initialization : Get vader score from txt file
    init_vader()

    # Possible modes
    mode = [
        'intensifier',
        'neutralizer',
        'uppercase',
        'threshold',
        'is_first',
        'is_last',
        'conjunction',
        'exclamation',
        'simple_neg',
        'not',
    ]

    # # Youtube Data
    # reviews = open_youtube("output.txt")[:100]
    # for review in reviews:
    #     youtube_score = get_score(review, mode)
    #     print("Review Text: %s" % review)
    #     print("Score Mode: %7.2f" % youtube_score)
    # return None

    # open corpus
    reader = Reader()
    lines = reader.open_csv(1, 0)

    # result
    result = []
    accuracy_naive = 0
    accuracy_mode = 0

    for idx, line in enumerate(lines):
        review = line[0]
        answer = float(line[1])
        # print(answer, review)

        # calculate score
        # score_naive = get_score(review, [])
        score_naive = 0
        score_mode = get_score(review, mode)
        print("score_naive: %7.2f, score_mode: %7.2f, answer: %5.2f" % (score_naive, score_mode, answer))

        # add difference with answer
        accuracy_naive += abs(score_naive - answer)
        accuracy_mode += abs(score_mode - answer)
        result.append([answer, score_naive, score_mode])

    # print overall accuracy
    print("accuracy_naive: %6.3f, accuracy_mode: %6.3f" % (accuracy_naive, accuracy_mode))

    # save
    csv_write("scoring_result.csv", result)


if __name__ == "__main__":
    main()
