import math

def compute_idf(docs):
    idf = {}
    for doc in docs:
        for term in doc:
            try:
                idf[term] += 1
            except KeyError:
                idf[term] = 1
    for k in idf:
        idf[k] = len(docs)/idf[k]
    return idf

def compute_tf(doc):
    tf = {}
    for term in doc:
        try:
            tf[term]
        except KeyError:
            tf[term] = doc.count(term)
    return tf

def compute_tfidf(idf, doc):
    tfidf = {}
    tf = compute_tf(doc)
    for k, v in tf.items():
        tfidf[k] = v * idf[k]
    return tfidf

def cosine(doc1, doc2):
    scalar = 0
    ldoc1 = 0
    ldoc2 = 0
    for term in set().union(*[doc1, doc2]):
        d1 = doc1.get(term, 0)
        d2 = doc2.get(term, 0)
        ldoc1 += math.pow(d1, 2)
        ldoc2 += math.pow(d2, 2)
        scalar += d1 * d2
    ldoc1, ldoc2 = math.sqrt(ldoc1), math.sqrt(ldoc2)
    return scalar/ (ldoc1 + ldoc2)


def rank(query, docs):
    results = []
    i = 0
    for doc in docs:
        results.append(
            {
                'cosine' : cosine(query, doc),
                'doc' : doc,
                'index' : str(i)
            }
        )
        i += 1
    return sorted(results, key=lambda x: x['cosine'], reverse=True)