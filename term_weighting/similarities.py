import math

def cosine(query, doc_vec):
    scalar = 0
    for k, v in query.items():
        try:
            scalar += v * doc_vec[k]
        except KeyError:
            pass
    length_query = math.sqrt(len(query))
    length_doc = 0
    for k, v in doc_vec.items():
        length_doc += math.pow(v, 2)
    length_doc = math.sqrt(length_doc)
    return scalar / (length_doc * length_query)

def euclidean(query, doc_vec):
    dist = 0
    union = set(dict(query, **doc_vec).keys())
    for k in union:
        try:
            dist += math.pow(query[k]-doc_vec[k], 2)
        except KeyError:
            try:
                dist += math.pow(query[k], 2)
            except KeyError:
                dist += math.pow(doc_vec[k], 2)
    return math.sqrt(dist)

def norm_euclidean(query, doc_vec):
    return euclidean(normalize_vector(query), normalize_vector(doc_vec))


def normalize_vector(vec):
    r = {}
    len = 0
    for k, v in vec.items():
        len += v
    for k,v in vec.items():
        r[k] = v/len
    return r