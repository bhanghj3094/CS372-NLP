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

    # evaluation for sentiment discrimination
    correct_cnt = 0
    wrong_cnt = 0
    neutral_cnt = 0

    for idx, line in enumerate(lines):
        review = line[0]
        answer = float(line[1])
        # print(answer, review)

        # calculate score
        score_naive = get_score(review, [])
        score_mode = get_score(review, mode)
        print("score_naive: %7.2f, score_mode: %7.2f, answer: %5.2f" % (score_naive, score_mode, answer))

        # add difference with answer
        accuracy_naive += abs(score_naive - answer)
        accuracy_mode += abs(score_mode - answer)
        result.append([answer, score_naive, score_mode])

        # Count correct, wrong. 
        is_correct = (answer > 3 and score_mode > 3) or \
                     (answer == 3 and 1.5 <= score_mode <= 4.5) or \
                     (answer < 3 and score_mode < 3)
        is_wrong = (answer > 3 and score_mode < 3) or \
                   (answer == 3 and (score_mode < 1.5 or score_mode > 4.5)) or \
                   (answer < 3 and score_mode > 3)
        assert not (is_correct and is_wrong)
        if is_correct: correct_cnt += 1
        elif is_wrong: wrong_cnt += 1
        else: neutral_cnt += 1

    # print overall accuracy
    print("accuracy_naive: %6.3f, accuracy_mode: %6.3f" % (accuracy_naive, accuracy_mode))

    # print overall discriminator performance
    total = correct_cnt + wrong_cnt + neutral_cnt
    print("True Positive: %6.3f" % (correct_cnt / total))
    print("False Positive: %6.3f" % (wrong_cnt / total))
    print("False Negative: %6.3f" % (neutral_cnt / total))
    
    precision = correct_cnt / (correct_cnt + wrong_cnt)
    recall = correct_cnt / (correct_cnt + neutral_cnt)
    print("Evaluation Schemes..")
    print("Precision: %6.3f" % (precision))
    print("Recall: %6.3f" % (recall))
    print("F-Score: %6.3f" % (2 * precision * recall / (precision + recall)))
    ####################################################
    # True Positive     : Correctly discriminated reviews. 
    # False Positive    : Wrongly discriminated reviews.
    # True Negative     : -- (None here)
    # False Negative    : Should have discriminated but couldn't. (Those with score 2.5, on rate 1,2,4,5)
    
    # Precision : TP / (TP + FP)
    # Recall    : TP / (TP + FN)
    # F-score   : (2 * Precision * Recall) / (Precision + Recall)
    ####################################################

    # save
    csv_write("scoring_result.csv", result)


if __name__ == "__main__":
    main()
