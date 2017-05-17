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

def compute_embedding_vec(embeddings, doc_tfidf):
    intersect = set(doc_tfidf.keys()).intersection(embeddings.keys())
    res = {}
    for term in intersect:
        divisor = 0
        a = 0
        _tfidf = doc_tfidf[term]
        divisor += _tfidf
        a += sum([float(_tfidf) * float(emb) for emb in embeddings[term]])
        res[term] = a / divisor
    return res
