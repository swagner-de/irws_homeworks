#! /usr/bin/env python3

import math

d1 = [0.17, 0.21, 0.35, 0.44, 0.49, 0.39, 0.09, 0.07, 0.37, 0.24]
d2 = [0.49, 0.48, 0.44, 0.09, 0.24, 0.2, 0.41, 0.16, 0.1, 0.15]
d3 = [0.41, 0.36, 0.27, 0.19, 0.15, 0.42, 0.23, 0.42, 0.02, 0.42]
d4 = [0.31, 0.41, 0.21, 0.19, 0.47, 0.28, 0.21, 0.39, 0.16, 0.38]
d5 = [0.46, 0.12, 0.21, 0.25, 0.38, 0.38, 0.46, 0.23, 0.31, 0.14]
d6 = [0.13, 0.33, 0.28, 0.42, 0.07, 0.13, 0.58, 0.15, 0.0, 0.49]
d7 = [0.21, 0.09, 0.07, 0.09, 0.3, 0.54, 0.24, 0.43, 0.51, 0.21]
d8 = [0.18, 0.39, 0.42, 0.05, 0.41, 0.1, 0.52, 0.12, 0.14, 0.38]
d9 = [0.4, 0.51, 0.01, 0.1, 0.12, 0.22, 0.26, 0.34, 0.42, 0.38]

dlist = [d1, d2, d3, d4, d5, d6, d7, d8, d9]

r1 = [0.33, 0.33, 0.42, 0.12, 0.2, 0.34, 0.58, 0.19, 0.07, 0.24]
r2 = [0.29, 0.16, 0.38, 0.48, 0.43, 0.11, 0.12, 0.33, 0.03, 0.44]
r3 = [0.01, 0.17, 0.11, 0.27, 0.23, 0.37, 0.35, 0.48, 0.54, 0.24]
r4 = [0.09, 0.05, 0.39, 0.25, 0.45, 0.48, 0.04, 0.45, 0.35, 0.12]
r5 = [0.13, 0.17, 0.4, 0.4, 0.07, 0.4, 0.35, 0.39, 0.44, 0.06]
rlist = [r1, r2, r3, r4, r5]

c1 = [0, 0, 1, 1, 0]
c2 = [0, 1, 1, 1, 0]
c3 = [0, 0, 0, 0, 0]
clist = [c1, c2, c3]

q = [0.15, 0.39, 0.36, 0.25, 0.36, 0.15, 0.52, 0.37, 0.08, 0.27]

def h(val):
    return 1 if val > 0.75 else 0


def scalar(d, r):
    res = 0
    for i in range(len(r)):
        res += d[i]*r[i]
    return res

def random_vector(d, rlist):
    return [scalar(d, rvec) for rvec in rlist]

def hashed_random_vector(d, rlist):
    vec = random_vector(d, rlist)
    return [h(val) for val in vec]

def vector_len(vec):
    len = 0
    for v in vec:
        len += math.pow(v, 2)
    return math.sqrt(len)

def cosine_sim(q, d):
    try:
        return scalar(d, q) / (vector_len(q) * vector_len(d))
    except ZeroDivisionError:
        return 0

def cluster(doc, clist):
    max=0
    for c in range(len(clist)):
        sim = cosine_sim(doc, clist[c])
        if sim >= max:
            max = sim
            l = c
    return l if not max == 0 else 0, max


def main():
    hashed_query = hashed_random_vector(q, rlist)
    query_leader, sim = cluster(hashed_query, clist)

    query_map = {}
    for k in range(len(dlist)):
        hashed = hashed_random_vector(dlist[k], rlist)
        print('d%s projected vector: %s' %(str(k+1), hashed))
        leader, sim = cluster(hashed, clist)
        print('\t matches best to cluster %s with similarity %s' % (str(leader+1), str(sim)))
        if query_leader == leader:
            query_map[k] = cosine_sim(hashed_query, hashed)

    s = sorted(query_map.items(), key=lambda x: x[1])

    print('Matching documents are:')
    print(s[len(s)-5:])

if __name__ == '__main__':
    main()