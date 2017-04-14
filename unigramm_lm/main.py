#! /usr/bin/env python3

import os
import logging
import argparse

from pprint import pprint
from doc_selector import get_random_docs
from preporcess import preprocess
from inverted_idx import *

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
    args = parser.parse_args()
    return args.files, args.amount


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
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    path, amount = parse_args()
    rand_docs = [doc for doc in get_random_docs(path, amount)]
    docs = [preprocess(doc) for doc in rand_docs]

    inv_idx = InvertedIdx()
    for idx in range(len(docs)-1):
        for term in docs[idx]:
            inv_idx.add_term(term, idx, docs)
    print(inv_idx)


if __name__ == '__main__':
    main()