import os
import glob
from random import randint


def get_all_filenames_rec(folder):
    return [filename for filename in glob.iglob(folder + '**', recursive=True) if not os.path.isdir(filename)]


def select_random_docsid(amount, total_docs):
    random_docs_id = set()
    while len(random_docs_id) < amount:
        random_docs_id.add(randint(0, total_docs-1))
    return random_docs_id


def load_docs(doc_ids, filenames):
    for idx in doc_ids:
        with open(filenames[idx], mode='r', encoding='cp1252') as file:
            yield file.read()
            file.close()


def get_random_docs(folder, amount):
    files = get_all_filenames_rec(folder)
    rand_doc_ids = select_random_docsid(amount, len(files))
    return load_docs(rand_doc_ids, files)
