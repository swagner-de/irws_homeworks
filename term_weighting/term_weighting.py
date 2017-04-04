#! /usr/bin/env python3

import nltk
from nltk.stem import WordNetLemmatizer
from pprint import pprint

d1 = "Frodo and Sam were trembling in the darkness, surrounded in darkness by hundreds of blood-thirsty orcs. Sam was certain these beasts were about to taste the scent of their flesh."
d2 = "The faceless black beast then stabbed Frodo. He felt like every nerve in his body was hurting. Suddenly, he thought of Sam and his calming smile. Frodo had betrayed him."
d3 = "Frodo’s sword was radiating blue, stronger and stronger every second. Orcs were getting closer. And these weren’t just regular orcs either, Uruk-Hai were among them. Frodo had killed regular orcs before, but he had never stabbed an Uruk-Hai, not wit the blue stick."
d4 = "Sam was carrying a small lamp, shedding some blue light. He was afraid that orcs might spot him, but it was the only way to avoid deadly pitfalls of Mordor."

blacklist = [

]



def filter_nouns_adjectives(tokens):
    tagged = nltk.pos_tag(tokens)
    return [t[0] for t in tagged if (t[1][:1] == 'J' or t[1][:1] == 'N') and t[0] not in blacklist]

def lemmatize(tokens):
    l = WordNetLemmatizer()
    return [l.lemmatize(t) for t in tokens]

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
        map[term] = len(docs)/occurences
    return map

def build_tf_map(doc):
    map = {}
    for t in doc:
        try:
            map[t]
        except KeyError:
            map[t] = doc.count(t)
    return map

def calc_tf_idf(tf, idf):
    vec = {}
    for k,v in tf.items():
        vec[k] = v*idf[k]
    return vec

def preprocess(docs):
    res = []
    for d in docs:
        tokens = nltk.word_tokenize(d)
        filtered = filter_nouns_adjectives(tokens)
        lemmatized = lemmatize(filtered)
        res.append(lemmatized)
    return res


def main():

    dlist = [d1.lower(), d2.lower(), d3.lower(), d4.lower()]

    dlist = preprocess(dlist)
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
        i += 1
        pprint(vector)



if __name__ == '__main__':
    main()