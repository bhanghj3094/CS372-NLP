import nltk
from SentimentDiscriminator import *
from autocorrect import Speller

spell = Speller(lang='en')

intensifiers = [word.strip() for word in open('intensifier.txt', 'r')]
stop_words = nltk.corpus.stopwords.words('english')

class Word():
    def __init__(self, text, pos_tag, is_intensifier, vader_score):
        self.text = text
        self.pos_tag = pos_tag
        self.is_intensifier = is_intensifier
        self.has_conjunction = text.isupper()
        self.vader_score = vader_score

class Sentence():
    def __init__(self, words, is_first, is_last, has_conjunction, has_multiple_exclamation):
        self.words = words
        self.is_first = is_first
        self.is_last = is_last
        self.has_conjunction = has_conjunction
        self.has_multiple_exclamation = has_multiple_exclamation
  
print(word_tokens) 
print(filtered_sentence)

def rate_five(score):
    """ Converts score to 0 ~ 5. """
    # if score[0] == 0 and score[1] == 0:
    #     return 2.5
    # else:
    #     return 5* score[0]/(score[0]+score[1])
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

    tagged_review = []
    sent_tokens = nltk.sent_tokenize(review)
    for i, sent_token in enumerate(sent_tokens):
        word_list = []
        has_conjunction = False
        for word, pos in nltk.pos_tag(nltk.tokenize.word_tokenize(sent_token)):
            if pos in ['CC','IN']:
                has_conjunction = True
            word = spell(word.lower())
            if word not in stop_words:
                word_list.append(Word(word, pos, word in intensifiers, get_vader_score(word) if get_vader_score(word) else stemmer(word)))
        tagged_review.append(Sentence(word_list, i == 0, i == len(sent_tokens) - 1, has_conjunction, sent_token.count('!') > 1))
        
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

# Initialization : Get vader score from txt file
init_vader()