import nltk
from .SentimentDiscriminator import *


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

    tagged_review = [
        nltk.pos_tag(nltk.word_tokenize(sent))
        for sent in nltk.sent_tokenize(review)
    ]
    for index, sentence in enumerate(tagged_review):
        for word, tag in sentence:
            if not check_word(word):
                continue
            # if verb, lemmatize.
            lemmatized_word = stemmer(word) if tag.startswith('v') else word
            new_score = get_sentiment(lemmatized_word, tag)

            # new_score is None on error. 
            if new_score:
                count += 1  # found score
                new_pos, new_neg, new_obj = new_score
                # sentence check
                is_conclusing = (index == len(tagged_review) - 1) or \
                                (index == len(tagged_review) - 2)
                if 'sent' in mode and is_conclusing:
                    new_pos *= 5
                    new_neg *= 5
                # negativity check
                if 'neg' in mode and neg_check == 1:
                    # reverse postivity and negativity. 
                    new_pos, new_neg = new_neg, new_pos
                neg_check = 1 if new_pos < new_neg else 0
                # add score
                score[0] += new_pos
                score[1] += new_neg

    score = [s * 100 / count for s in score] if count != 0 else score
    return rate_five(score)
