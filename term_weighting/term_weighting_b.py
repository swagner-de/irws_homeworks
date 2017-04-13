#! /usr/bin/env python3

import nltk
import math
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from pprint import pprint

lemmatizer = WordNetLemmatizer()


d1 = "Frodo and Sam were trembling in the darkness, surrounded in darkness by hundreds of blood-thirsty orcs. Sam was certain these beasts were about to taste the scent of their flesh."
d2 = "The faceless black beast then stabbed Frodo. He felt like every nerve in his body was hurting. Suddenly, he thought of Sam and his calming smile. Frodo had betrayed him."
d3 = "Frodo's sword was radiating blue, stronger and stronger every second. Orcs were getting closer. And these weren't just regular orcs either, Uruk-Hai were among them. Frodo had killed regular orcs before, but he had never stabbed an Uruk-Hai, not wit the blue stick."
d4 = "Sam was carrying a small lamp, shedding some blue light. He was afraid that orcs might spot him, but it was the only way to avoid deadly pitfalls of Mordor."

d1_rel = "Frodo Sam darkness surrounded darkness blood-thirsty orc. Sam certain beast scent flesh."
d2_rel = "faceless black beast Frodo. nerve body. Sam calming smile. Frodo."
d3_rel = "Frodo sword radiating blue, stronger stronger second. Orc closer. regular orc, Uruk-Hai. Frodo regular orc Uruk-Hai blue stick."
d4_rel = "Sam small lamp, blue light. afraid orc way deadly pitfalls Mordor."

q= ['sam', 'blue', 'orc']


corrections = {
    'orcs' : 'orc',
    'only' : None,
}

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


def filter_nouns_adjectives(tokens):
    tagged = nltk.pos_tag(tokens)
    for t in tagged:
        if (t[1][:1] == 'J' or t[1][:1] == 'N'):
            yield t


def lemmatize(tokens):
    for t in tokens:
        try:
            yield lemmatizer.lemmatize(t[0], get_wordnet_pos(t[1]))
        except KeyError:
            pass


def manual_correct(tokens):
    for t in tokens:
        try:
            replacement = corrections[t]
            if replacement:
                yield replacement
        except KeyError:
            yield t


def build_idf_map(docs):
    all_terms = set()
    for d in docs:
        for t in d:
            all_terms.add(t)
    map = {}
    for term in all_terms:
        occurences = 0
        for d in docs:
            occurences += 1 if term in d else 0
        map[term] = (len(docs) - occurences) / occurences
    return map

def build_tf_map(doc):
    map = {}
    max_term_freq = 0
    for t in doc:
        max_term_freq = doc.count(t) if doc.count(t) > max_term_freq else max_term_freq
    for t in doc:
        try:
            map[t]
        except KeyError:
            map[t] = (1 + math.log2(doc.count(t))) / (1 + math.log2(max_term_freq))
    return map

def calc_tf_idf(tf, idf):
    vec = {}
    for k,v in tf.items():
        vec[k] = v*idf[k]
    return vec

def preprocess(docs, filter=True):
    res = []
    for d in docs:
        tokens = nltk.word_tokenize(d)
        filtered_and_tagged = filter_nouns_adjectives(tokens) if filter else nltk.pos_tag(tokens)
        lemmatized = lemmatize(filtered_and_tagged)
        corrected = manual_correct(lemmatized)
        res.append([t for t in corrected])
    return res


def main():

    query = {}
    for t in q:
        query[t] =1.0

    dlist = [d1.lower(), d2.lower(), d3.lower(), d4.lower()]

    drlist = [d1_rel.lower(), d2_rel.lower(), d3_rel.lower(), d4_rel.lower()]

    #dlist = preprocess(dlist)
    dlist = preprocess(drlist, filter=False)
    print('Filtered and lemmatized:')
    i = 1
    for d in dlist:
        print('doc%s : ' % str(i) + ', '.join(d))
        i += 1
    print('************************************************')

    idf_map = build_idf_map(dlist)
    print('IDF scores')
    pprint(idf_map)
    print('************************************************')

    i = 1
    for doc in dlist:
        tf_map = build_tf_map(doc)
        vector = calc_tf_idf(tf_map, idf_map)
        print('--doc%s--' % (str(i)))
        pprint(vector)
        sim = cosine(query, vector)
        print('Cosine similarity doc%s and query: %s' % (str(i), str(sim)))
        i += 1



if __name__ == '__main__':
    main()