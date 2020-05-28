import nltk, csv, os
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from nltk.stem.lancaster import LancasterStemmer
from dataset.csvReader import Reader

######### Helper Functions ########

def additional_stemmer(word):
    """ Additional stemmer (You can add more pattern) """
    if word == "n't":
        return "not"
    elif word.endswith("n't"):
        return word.split("n't")[0] + " not"
    return word

def stemmer(word):
    """ Stemmer for use """
    word = additional_stemmer(word)
    return LancasterStemmer().stem(word)


def synset_name(synset):
    """ function to change synset into string """
    return synset.name().split(".")[0]


def find_wn_synset(word, pos):
    """ function to find wordnet synset with input word and POS """
    synsets = wn.synsets(word)
    for synset in synsets:
        if synset_name(synset) == word and synset.pos() == pos:
            return synset
    if len(synsets) == 0:
        return None
    return synsets[0]


def check_word(word):
    """ function to check if the word is normal word """
    if not word.isalpha():
        if (
            not (word.endswith(",") or word.endswith("."))
            and not word[: len(word) - 2].isalpha()
        ):
            return False
    return True


def tag_convert(tag):
    """ function to convert nltk.tag to wordnet tag """
    if tag in ["RB", "RBR", "RBS"]:
        return "r"
    elif tag in ["JJ", "JJR", "JJS"]:
        return "a"
    elif tag in ["VB", "VBD", "VBG", "VBN", "VBP", "VBZ"]:
        return "v"
    elif tag.startswith("N"):
        return "n"
    return None


######### Main Functions #########

def additional_sentiment(word, tag):
    """ Additional sentiment calculator (You can add more pattern) """
    if word == "great":
        return [1,0,0]
    elif word == "comfortable" or word == "comfy":
        return [0.5,0,0]
    return None

def get_sentiment(word, tag):
    """ returns (pos, neg, obj) score of input word. Returns None if error """
    if not additional_sentiment(word, tag) == None:
        return additional_sentiment(word, tag)
    wn_tag = tag_convert(tag)
    if wn_tag is None:
        return None
    wn_synset = find_wn_synset(word, wn_tag)
    if wn_synset is None:
        return None
    # Take the first sense, the most common
    swn_synset = swn.senti_synset(wn_synset.name())
    return [
        swn_synset.pos_score() ** 2,
        swn_synset.neg_score() ** 2,
        swn_synset.obj_score() ** 2,
    ]

# original version without any additional methods
def get_score_org(review):
    """ Calculate own score by tokenized words' negativity/positivity """
    # Initialize scores
    score = [0, 0]
    cnt = 0

    tagged_word_list = nltk.pos_tag(nltk.word_tokenize(review))
    for tagged_word in tagged_word_list:
        if not check_word(tagged_word[0]):
            continue
        if tagged_word[1].startswith('V'):
            lemmatized_word = stemmer(tagged_word[0])
            new_score = get_sentiment(lemmatized_word, tagged_word[1])
        else:
            new_score = get_sentiment(tagged_word[0], tagged_word[1])

        if not new_score is None:
            for i in range(2):
                score[i] += new_score[i]
            if score[0] != 0 or score[1] != 0:
                cnt += 1
    if cnt == 0:
        return [0, 0]
    else:
        return [s * 100 / cnt for s in score]


# *5 scores in last two stc.
def get_score(review):
    """ Calculate own score by tokenized words' negativity/positivity """
    # Initialize scores
    score = [0, 0]
    cnt = 0
    words = nltk.sent_tokenize(review)
    for sent in range(len(words)):
        tagged_word_list = nltk.pos_tag(nltk.word_tokenize(words[sent]))
        for tagged_word in tagged_word_list:
            if not check_word(tagged_word[0]):
                continue
            if tagged_word[1].startswith('V'):
                lemmatized_word = stemmer(tagged_word[0])
                new_score = get_sentiment(lemmatized_word, tagged_word[1])
            else:
                new_score = get_sentiment(tagged_word[0], tagged_word[1])

            if not new_score is None:
                for i in range(2):
                    if sent == (len(words) - 1) or sent == (len(words) - 2):
                        new_score[i] *= 5
                    score[i] += new_score[i]
                if score[0] != 0 or score[1] != 0:
                    cnt += 1
    if cnt == 0:
        return [0, 0]
    else:
        return [s * 100 / cnt for s in score]


def get_score_with_neg_check(review):
    """ Calculate own score by tokenized words' negativity/positivity and double negation check """
    # Initialize scores
    score = [0, 0]
    cnt = 0
    neg_check = 0
    tagged_word_list = nltk.pos_tag(nltk.word_tokenize(review))
    for tagged_word in tagged_word_list:
        if not check_word(tagged_word[0]):
            continue
        if tagged_word[1].startswith('V'):
            lemmatized_word = stemmer(tagged_word[0])
            new_score = get_sentiment(lemmatized_word, tagged_word[1])
        else:
            new_score = get_sentiment(tagged_word[0], tagged_word[1])

        if not new_score is None:
            if neg_check == 1:
                new_score[0], new_score[1] = new_score[1], new_score[0]
            for i in range(2):
                score[i] += new_score[i]
            if score[0] != 0 or score[1] != 0:
                cnt += 1
            if score[0] < score[1]:
                neg_check = 1
            elif score[1] >= score[0]:
                neg_check = 0

    if cnt == 0:
        return [0, 0]
    else:
        return [s * 100 / cnt for s in score]


def rate_five(score):
    """ Converts score to 0 ~ 5. """
    # if score[0] == 0 and score[1] == 0:
    #     return 2.5
    # else:
    #     return 5* score[0]/(score[0]+score[1])
    return score[0] - score[1]


def csv_write(file_name, result):
    csv_file = open(file_name, "w")
    
    # header
    csv_file.write("Rate, Score-1, Score-2\n")

    for entry in result:
        entry_to_string = ", ".join([str(e) for e in entry])
        csv_file.write(entry_to_string + "\n")
    csv_file.close()


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
    score_naive = rate_five(get_score(review))
    score_neg = rate_five(get_score_with_neg_check(review))
    print("score_naive: %7.2f, score_neg: %7.2f, answer: %5.2f" % (score_naive, score_neg, answer))
    
    # add difference with answer
    accuracy_naive += abs(score_naive - answer)
    accuracy_neg += abs(score_neg - answer)
    result.append([answer, score_naive, score_neg])

# print overall accuracy
print("accuracy_naive: %6.3f, accuracy_neg: %6.3f" % (accuracy_naive / len(lines), accuracy_neg / len(lines)))

# save
csv_write("scoring_result.csv", result)
