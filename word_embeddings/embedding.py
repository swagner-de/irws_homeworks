import glob
import os
import numpy as np


def load_emebeddings(folder):
    files = [filename for filename in glob.iglob(folder + '**', recursive=True) if not os.path.isdir(filename)]
    w2v = {}
    for file in files:
        with open(file, "r", encoding='utf8') as lines:
            for line in lines:
                # based on http://nadbordrozd.github.io/blog/2016/05/20/text-classification-with-word2vec/
                w2v[line.split()[0]] = line.split()[1:]
    return w2v

# derive a vector by multiplying the tfidf with every line of the embeddingg vector
# then sum all embedding vectors together
# then divide by the sum of the length of all embedding vectors
def compute_embedding_vec(embeddings, doc_tfidf):
    intersect = set(doc_tfidf.keys()).intersection(embeddings.keys())
    res = []
    divisor = 0
    for term in intersect:
        _tfidf = doc_tfidf[term]
        divisor += _tfidf
        emb_vec = embeddings[term]
        for emb in range(len(emb_vec)):
            try:
                res[emb] += _tfidf * float(emb_vec[emb])
            except IndexError:
                res.append(_tfidf * float(emb_vec[emb]))
    for k in res:
        k /= divisor
    return res
