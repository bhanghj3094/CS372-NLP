import nltk
from nltk.stem import WordNetLemmatizer
from autocorrect import Speller
from .SentimentDiscriminator import *


# Global variables
speller = Speller(lang='en')
lemmatizer = WordNetLemmatizer().lemmatize
intensifiers = [word.strip() for word in open('algorithm/intensifier.txt', 'r')]
stopwords = nltk.corpus.stopwords.words('english')


class Word():
    def __init__(self, text, pos_tag, is_intensifier, vader_score):
        self.text = text
        self.pos_tag = pos_tag
        self.is_intensifier = is_intensifier
        self.is_uppercase = text.isupper()
        self.vader_score = vader_score


class Sentence():
    def __init__(self, words, is_first, is_last, has_conjunction, has_multiple_exclamation):
        self.words = words
        self.is_first = is_first
        self.is_last = is_last
        self.has_conjunction = has_conjunction
        self.has_multiple_exclamation = has_multiple_exclamation


def tokenizer(sent):
    """Sentence tokenizer with removing - in words """
    tokenized_list = nltk.word_tokenize(sent)
    for i, word in enumerate(tokenized_list):
        if "-" in word:
            seperated_words = word.split("-")
        elif word.endswith("n't"):
            seperated_words = [word[:-3], 'not']
        else:
            continue

        # if modified
        tokenized_list.pop(i)
        for word in seperated_words[::-1]:
            tokenized_list.insert(i, word)
    return nltk.pos_tag(tokenized_list)


def rate_five(score):
    """ Converts score to 0 ~ 5. """
    return score[0] - score[1]


def get_score(review, mode=[]):
    """ Calculate positivity/negativity of review. 

    Args:
        review (String): text of review. 
        mode (List): list of modes to apply. 
            'sent' - additional scores to sentences.
            'neg' - check double negation.
    
    Returns:
        score (Tuple): [positivity_score, negativity_score]
    """
    count = 0  # number of words with score. 
    neg_check = 0  # variable to hold former word's negativity.
    score = [0, 0]

    sentences = []
    tokenized_sentences = nltk.sent_tokenize(review)
    for idx, sentence in enumerate(tokenized_sentences):
        word_list = []
        has_conjunction = False
        for word, pos in tokenizer(sentence):
            if pos in ['CC','IN'] and word not in stopwords:
                has_conjunction = True
            word = speller(word)
            vader_score = get_vader_score(word) if get_vader_score(word) else get_vader_score(lemmatizer(word))
            new_word = Word(word, pos, word in intensifiers, vader_score)
            word_list.append(new_word)
        is_first, is_last = idx == 0, idx == len(tokenized_sentences) - 1
        new_sentence = Sentence(word_list, is_first, is_last, has_conjunction, sentence.count('!') > 1)
        sentences.append(new_sentence)


    # tagged_review = [
    #     nltk.pos_tag(nltk.word_tokenize(sent))
    #     for sent in nltk.sent_tokenize(review)
    # ]
    # for index, sentence in enumerate(tagged_review):
    #     for word, tag in sentence:
    #         if not check_word(word):
    #             continue
    #         # if verb, lemmatize.
    #         lemmatized_word = stemmer(word) if tag.startswith('v') else word
    #         new_score = get_sentiment(lemmatized_word, tag)

    #         # new_score is None on error. 
    #         if new_score:
    #             count += 1  # found score
    #             new_pos, new_neg, new_obj = new_score
    #             # sentence check
    #             is_conclusing = (index == len(tagged_review) - 1) or \
    #                             (index == len(tagged_review) - 2)
    #             if 'sent' in mode and is_conclusing:
    #                 new_pos *= 5
    #                 new_neg *= 5
    #             # negativity check
    #             if 'neg' in mode and neg_check == 1:
    #                 # reverse postivity and negativity. 
    #                 new_pos, new_neg = new_neg, new_pos
    #             neg_check = 1 if new_pos < new_neg else 0
    #             # add score
    #             score[0] += new_pos
    #             score[1] += new_neg

    # score = [s * 100 / count for s in score] if count != 0 else score
    # return rate_five(score)
    return 0

# Initialization : Get vader score from txt file
init_vader()