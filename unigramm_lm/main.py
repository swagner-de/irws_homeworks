#! /usr/bin/env python3

import os
import logging
import argparse

from pprint import pprint
from doc_selector import get_random_docs
from preprocess import preprocess
from inverted_idx import *
from query import Query

LOGGER = logging.getLogger()

global docs

def parse_args():
    """
    initiates the argparseres and returns configpath gotten from parser
    """
    parser = argparse.ArgumentParser(
        description='Unigramm LM', prog='unigramm_lm')

    parser.add_argument(
        '-f',
        type=str,
        nargs='?',
        dest='files',
        required=True,
        help='path to files')
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
    return args.files, args.amount, args.query_terms.lower()


def init_logging(log_path):
    """
    This will initiate the logging by setting the loglevel and creating a loghandler
    """
    LOGGER.setLevel(logging.INFO)
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter('%(levelname)s %(asctime)s %(message)s')
    stream_handler.setFormatter(formatter)
    LOGGER.addHandler(stream_handler)

def main():
    # initialize
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    path, amount, query_terms = parse_args()

    # load random docs in memory
    rand_docs = [doc for doc in get_random_docs(path, amount)]
    # preprocess these docs
    docs = [preprocess(doc) for doc in rand_docs]

    inv_idx = InvertedIdx()
    inv_idx.build_idx_from_docs(docs)

    print('Inverted index')
    print(inv_idx)
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

    global_unigramm = build_global_unigram(inv_idx)

    print('global unigramm model')
    pprint(global_unigramm)
    print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')

    q = Query(query_terms.split(' '), docs, inv_idx)


if __name__ == '__main__':
    main()