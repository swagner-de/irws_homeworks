import string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import TreebankWordTokenizer
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet


TOKENIZER = TreebankWordTokenizer()
LEMMATIZER = WordNetLemmatizer()
STOP = stopwords.words('english')


# stolen from http://stackoverflow.com/questions/15586721/wordnet-lemmatization-and-pos-tagging-in-python
def get_wordnet_pos(treebank_tag):
    if treebank_tag.startswith('J'):
        return wordnet.ADJ
    elif treebank_tag.startswith('V'):
        return wordnet.VERB
    elif treebank_tag.startswith('N'):
        return wordnet.NOUN
    elif treebank_tag.startswith('R'):
        return wordnet.ADV
    else:
        return ''


def tokenize(doc):
    doc = " ".join("".join([" " if ch in string.punctuation else ch for ch in doc]).split())
    for token in TOKENIZER.tokenize(doc):
        yield token.lower()


def remove_stopwords(tokens):
    res = []
    for token in tokens:
        if token not in STOP:
            res.append(token)
    return res


def lemmatize(tokens):
    tagged = nltk.pos_tag(tokens)
    for t in tagged:
        try:
            yield LEMMATIZER.lemmatize(t[0], get_wordnet_pos(t[1]))
        except KeyError:
            pass

def preprocess(doc):
    tokens = tokenize(doc)
    tokens = remove_stopwords(tokens)
    return tokens

