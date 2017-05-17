#! /usr/bin/env python3

import os
import argparse

from doc_selector import get_random_docs
from preprocess import preprocess
from pprint import pprint
import tfidf
import embedding


def parse_args():
    """
    initiates the argparseres and returns configpath gotten from parser
    """
    parser = argparse.ArgumentParser(
        description='word embeddings', prog='word_embeddings')

    parser.add_argument(
        '-f',
        type=str,
        nargs='?',
        dest='files',
        required=True,
        help='path to newsgroup files')
    parser.add_argument(
        '-e',
        type=str,
        nargs='?',
        dest='embeddings',
        required=True,
        help='path to embeddings')

    parser.add_argument(
        '-a',
        type=int,
        nargs='?',
        dest='amount',
        required=True,
        help='amount of selected docs')
    parser.add_argument(
        '-q',
        type=str,
        nargs='?',
        dest='query_terms',
        required=True,
        help='terms for query')
    args = parser.parse_args()
    return args.files, args.embeddings, args.amount, args.query_terms.lower().split(' ')


def main():
    # initialize
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    news_path, embeddings_path, amount, query_terms = parse_args()

    rand_docs = get_random_docs(news_path, amount)

    preprocessed = [preprocess(doc) for doc in rand_docs]

    idf = tfidf.compute_idf(preprocessed)
    tfidfs_ = [tfidf.compute_tfidf(idf, doc) for doc in preprocessed]

    emb = embedding.load_emebeddings(embeddings_path)
    embedding_vecs = [embedding.compute_embedding_vec(emb, tfidf_) for tfidf_ in tfidfs_]

    query_tfidf = tfidf.compute_tfidf(idf, query_terms)
    query_embedded = embedding.compute_embedding_vec(emb, query_tfidf)

    ranked = tfidf.rank(query_embedded, embedding_vecs)

    pprint(ranked[:10])

if __name__ == '__main__':
    main()