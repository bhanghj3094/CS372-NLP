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
        # TODO: add more patterns
        if "-" in word:
            seperated_words = [ e for e in word.split("-") if e ]
        elif word == "n't":
            tokenized_list[i] = 'not'
            continue
        else:
            continue
        # if modified
        tokenized_list.pop(i)
        for word in seperated_words[::-1]:
            tokenized_list.insert(i, word)
    return nltk.pos_tag(tokenized_list)


# UNUSED
def rate_five(score):
    """ Converts score to 0 ~ 5. """
    return score[0] - score[1]


def get_score(review, mode=[]):
    """ Calculate positivity/negativity of review. 

    Args:
        review (String): text of review. 
        mode (List): list of modes to apply. 
            # words
            'intensifier' - give weight on word behind intensifiers
            'uppercase' - check if word is upper
            'threshold' - ignore small scores
            # sentences
            'is_first' - weight on first sentence
            'is_last' - weight on last sentence
            'conjunction' - weight on conjunctions
            'exclamation' - weight on exclamations
            # relations
            'simple_neg' - check double negation.
            'not' - check negation by 'not'.
    
    Returns:
        score (Tuple): [positivity_score, negativity_score]
    """
    count = 0  # number of words with score. 
    neg_check = 0  # variable to hold former word's negativity.
    score = [0, 0]

    sentences = []
    tokenized_sentences = nltk.sent_tokenize(review)
    for idx, sentence in enumerate(tokenized_sentences):
        words = []
        has_conjunction = False
        for word, pos in tokenizer(sentence):
            if pos in ['CC','IN'] and word not in stopwords:
                has_conjunction = True
            word = speller(word)
            vader_score = get_vader_score(word) if get_vader_score(word) else get_vader_score(lemmatizer(word))
            # print([word, pos, word in intensifiers, vader_score])
            new_word = Word(word, pos, word in intensifiers, vader_score)
            words.append(new_word)
        is_first, is_last = idx == 0, idx == len(tokenized_sentences) - 1
        # print([is_first, is_last, has_conjunction, sentence.count('!') > 1])
        new_sentence = Sentence(words, is_first, is_last, has_conjunction, sentence.count('!') > 1)
        sentences.append(new_sentence)

    sentence_scores = []  # sentence score, importance
    for sentence in sentences:
        # Iterate words
        valid_word_count = 0
        intensifier_check = False
        simple_negative_check = False
        not_check = False

        # Initialize sentence score
        sentence_score = 0
        for word in sentence.words:
            word_score = word.vader_score
            if 'intensifier' in mode:
                if intensifier_check:
                    word_score *= 2
                intensifier_check = True if word.is_intensifier else False
            if 'uppercase' in mode and word.is_uppercase:
                word_score *= 2
            if 'threshold' in mode and abs(word.vader_score) < 0.3:
                word_score = 0
            # Negativity check
            if 'simple_neg' in mode:
                if simple_negative_check:
                    word_score *= -1
                simple_negative_check = True if word_score < 0 else False
            if 'not' in mode:
                if not_check:
                    word_score *= -1
                not_check = True if word == 'not' else False
            # Count words with score
            if word_score != 0: valid_word_count += 1
            sentence_score += word_score
        
        # Pure sentence score
        sentence_score = sentence_score / valid_word_count if valid_word_count != 0 else 0
        sentence_importance = valid_word_count

        if 'is_first' in mode and sentence.is_first:
            sentence_importance *= 2
        if 'is_last' in mode and sentence.is_last:
            sentence_importance *= 2
        if 'conjunction' in mode and sentence.has_conjunction:
            sentence_importance *= 2
        if 'exclamation' in mode and sentence.has_multiple_exclamation:
            sentence_importance *= 2        
        sentence_scores.append((sentence_score, sentence_importance))
    
    # Calculate overall score
    total_importance = sum([impt for _, impt in sentence_scores])
    # Nullity check
    if total_importance == 0: 
        return 0
    total_score = sum([ score * impt / total_importance for score, impt in sentence_scores])
    return total_score
