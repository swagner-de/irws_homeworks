#!/usr/bin/env python3
import os
import json



def read_terms(path):
    with open(path, mode='r', encoding='utf8') as file:
        return file.read().splitlines()

def permute(terms):
    for term in terms:
        term +='$'
        t_len = len(term)
        for i in range(0,t_len):
            yield term[i:]+term[:i]

def gen_key(l):
    beg = l[0]
    beg = beg.split(' - ')[0]
    end = l[len(l)-1]
    try:
        end = end.split(' - ')[1]
    except IndexError:
        end = end
    beg = beg.replace("'", "")
    end = end.replace("'", "")

    return "'%s' - '%s'" % (beg, end)


def initial_grouping(terms, branching_factor):
    result = {}
    l = []
    for i in range(len(terms)):
        l.append(terms[i])
        if i % branching_factor == 2:
            result[gen_key(l)] = l
            l =[]
    return result

def group(d, branching_factor):
    top = {}
    inner = {}
    i = 0
    for k,v in d.items():
        inner[k] = v
        if i % branching_factor == 2:
            top[gen_key([k for k in inner.keys()])] = inner
            inner = {}
        i += 1
    if len(top) < branching_factor: return group(top, branching_factor)
    else: return top


def export_as_json(d, file):
    j = json.dumps(d, sort_keys=True, indent=4, separators=(',', ': '))
    with open(file, mode='w', encoding='utf8') as file:
        file.writelines(j)


def main():
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    terms = read_terms('terms.txt')
    permutations = [t for t in permute(terms)]
    permutations.sort()
    init_grouped = initial_grouping(permutations, 3)
    grouped = group(init_grouped, 3)
    export_as_json(grouped, "perm_index.json")

if __name__ == '__main__':
    main()