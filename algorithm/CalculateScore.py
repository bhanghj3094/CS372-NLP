import nltk
from nltk.stem import WordNetLemmatizer
from autocorrect import Speller
from .SentimentDiscriminator import *
from pprint import pprint


# Global variables
speller = Speller(lang='en')
lemmatizer = WordNetLemmatizer().lemmatize
intensifiers = [word.strip() for word in open('algorithm/intensifier.txt', 'r') if word.strip().isalpha()]
neutralizers = [word.strip() for word in open('algorithm/neutralizer.txt', 'r') if word.strip().isalpha()]
stopwords = nltk.corpus.stopwords.words('english')


class Word():
    def __init__(self, text, pos_tag, is_intensifier, is_neutralizer, vader_score):
        self.text = text
        self.pos_tag = pos_tag
        self.is_intensifier = is_intensifier
        self.is_neutralizer = is_neutralizer
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
            'neutralizer' - lower weight on word behind neutralizers
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
            spelled_word = speller(word.lower())
            vader_score = get_vader_score(spelled_word) if get_vader_score(spelled_word) else get_vader_score(lemmatizer(spelled_word))
            new_word = Word(word, pos, spelled_word in intensifiers, spelled_word in neutralizers, vader_score)
            words.append(new_word)
        is_first, is_last = idx == 0, idx == len(tokenized_sentences) - 1
        new_sentence = Sentence(words, is_first, is_last, has_conjunction, sentence.count('!') > 1)
        sentences.append(new_sentence)

    sentence_scores = []  # sentence score, importance
    for sentence in sentences:
        # Check variables
        intensifier_check = False
        neutralizer_check = False
        simple_negative_check = False
        not_check = False
        
        # Iterate words
        word_scores = []
        valid_word_count = 0
        for word_idx, word in enumerate(sentence.words):
            word_score = word.vader_score
            if 'intensifier' in mode:
                if intensifier_check:
                    word_score *= 2
                intensifier_check = True if word.is_intensifier else False
            if 'neutralizer' in mode:
                if neutralizer_check:
                    word_score /= 2
                neutralizer_check = True if word.is_neutralizer else False
            if 'uppercase' in mode and word.is_uppercase:
                word_score *= 2
            if 'threshold' in mode and abs(word.vader_score) < 0.3:
                word_score = 0
            # Negativity check
            if 'simple_neg' in mode:
                if simple_negative_check and not not_check:
                    word_score *= -1
                simple_negative_check = True if word_score < 0 else False
            if 'not' in mode:
                if not_check:
                    word_score *= -1
                    word_scores[word_idx-1][2] *= -1
                    if word_score == 0:
                        word_scores[word_idx-1][2] = 0
                not_check = True if word.text in ['not','no'] else False
            if word_score != 0: valid_word_count += 1
            word_scores.append([word.text, word.is_intensifier, word_score])
        print("word_scores:", word_scores)
        word_scores = [score for word, _, score in word_scores]

        # Pure sentence score
        sentence_score = sum(word_scores) / valid_word_count if valid_word_count != 0 else 0
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

    print("score, importance:", sentence_scores)

    # Calculate overall score
    total_importance = sum([impt for _, impt in sentence_scores])
    # Nullity check
    if total_importance == 0: 
        return 2.5
    total_score = sum([ score * impt / total_importance for score, impt in sentence_scores])
    return total_score + 2.5
