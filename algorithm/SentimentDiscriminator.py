import nltk, os.path
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from collections import defaultdict


######### Helper Functions ########
# UNUSED
def synset_name(synset):
    """ function to change synset into string """
    return synset.name().split(".")[0]


# UNUSED
def find_wn_synset(word, pos):
    """ function to find wordnet synset with input word and POS """
    synsets = wn.synsets(word)
    for synset in synsets:
        if synset_name(synset) == word and synset.pos() == pos:
            return synset
    if len(synsets) == 0:
        return None
    return synsets[0]


# UNUSED
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


# UNUSED
def additional_sentiment(word, tag):
    """ Additional sentiment calculator (You can add more pattern) """
    if word == "great":
        return [1,0,0]
    elif word == "comfortable" or word == "comfy":
        return [0.5,0,0]
    return None


# UNUSED
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


######### Main Functions #########
vader_score = defaultdict(int)
special_words = []

def init_vader():
    """ Initializing vader score """
    f = open("algorithm/vader_lexicon.txt", "r")
    while True:
        line = f.readline()
        if not line: break
        token, score, _, _ = line.strip().split('\t')     # list of [TOKEN, MEAN-SENTIMENT-RATING, STANDARD DEVIATION, RAW-HUMAN-SENTIMENT-RATINGS]
        vader_score[token] = score
    f.close()
    f = open("algorithm/special_words.txt", "r")
    while True:
        line = f.readline()
        if not line: break
        token, score, _, _ = line.strip().split('\t')     # list of [TOKEN, MEAN-SENTIMENT-RATING, STANDARD DEVIATION, RAW-HUMAN-SENTIMENT-RATINGS]
        special_words.append((token,score))
    f.close()


def get_vader_score(word):
    """ Return vader score. """
    return float(vader_score[word.lower()])

def get_special_score(sent):
    """ Return special score. """
    result = 0
    for special_word in special_words:
        if special_word[0] in sent:
            result += float(special_word[1])
    return result