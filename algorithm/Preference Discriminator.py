import nltk
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag
from nltk.corpus import wordnet as wn
from nltk.corpus import sentiwordnet as swn
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

######### Helper Functions ########

def synset_name(synset):
    """ function to change synset into string """
    return synset.name().split('.')[0]

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
        if not (word.endswith(',') or word.endswith('.')) and not word[:len(word)-2].isalpha():
            return False
    return True

def tag_convert(tag):
    """ function to convert nltk.tag to wordnet tag """
    if tag in ['RB', 'RBR', 'RBS']:
        return 'r'
    elif tag in ['JJ', 'JJR', 'JJS']:
        return 'a'
    elif tag in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
        return 'v'
    elif tag.startswith('N'):
        return 'n'
    return None

######### Main Functions #########

def get_sentiment(word, tag):
    """ returns (pos, neg, obj) score of input word. Returns None if error """
    wn_tag = tag_convert(tag)
    if wn_tag is None:
        return None
    wn_synset = find_wn_synset(word, wn_tag)
    if wn_synset is None:
        return None
    # Take the first sense, the most common
    swn_synset = swn.senti_synset(wn_synset.name())
    return [swn_synset.pos_score(), swn_synset.neg_score(), swn_synset.obj_score()]

def get_score(review):
    # Initialize scores
    score = [0, 0]
    cnt = 0
    tagged_word_list = nltk.pos_tag(nltk.word_tokenize(review))
    for tagged_word in tagged_word_list:
        if not check_word(tagged_word[0]):
            continue
        if tagged_word[1].startswith('V'):
            lemmatized_word = stemmer.stem(tagged_word[0])
            new_score = get_sentiment(lemmatized_word, tagged_word[1])
        else:
            new_score = get_sentiment(tagged_word[0], tagged_word[1])
        if not new_score is None:
            for i in range (2):
                score[i] += new_score[i]
            cnt += 1
    return [s*100/cnt for s in score]

# Get input
# For now, just get input manually
# review = input()
good_review = "This place is really nice! The food is good (they have seasonal rotations, so the menu changes often). I’ve been a few times and have always left satisfied. The workers are really friendly. They have good vegetarian options, and I like their coffee. Only downside is it’s a little pricey. It’s a cute place to go, though, and you can browse books after you eat! The book selection is good for a small, local bookstore. It’s not a place I’d go all the time, but it’s really fun to bring visitors to and a great option if you’re in the area."
bad_review = "My first experience with Jimmy John's was this location and I have to admit it will be my last. The guy who waited on me was extremely unprofessional, he didn't give me any idea of the order process and got extremely short with me when placing my order. When repeating my order, he spoke so fast I couldnt understand what he said so I ordered something I didnt want. Then realizing I wasn't asked what I wanted on my sandwich specifically, so I went back over to confirm my order. This guy actually gave me an attitude and sighed (loudly)when I wanted my sandwich corrected without meat before it even made! I waited for my sandwich and I was told he was the GENERAL MANAGER! The staff of ladies were on point and apologized for his behavior. Unfortunately the tasty sandwich didn't make-up for his nasty attitude."

print(get_score(good_review))
print(get_score(bad_review))