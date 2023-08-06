#!/usr/bin/env python3

import argparse
import logging
import multiprocessing
import time

from somajo import Tokenizer
from somajo import SentenceSplitter


def arguments():
    """"""
    parser = argparse.ArgumentParser(description="Tokenize an input file according to the guidelines of the EmpiriST 2015 shared task on automatic linguistic annotation of computer-mediated communication / social media.")
    parser.add_argument("-s", "--paragraph_separator", choices=["empty_lines", "single_newlines"], default="empty_lines", help="How are paragraphs separated in the input text? (Default: empty_lines)")
    parser.add_argument("-c", "--split_camel_case", action="store_true", help="Split items in written in camelCase (excluding several exceptions).")
    parser.add_argument("-t", "--token_classes", action="store_true", help="Output the token classes (number, XML tag, abbreviation, etc.) in addition to the tokens.")
    parser.add_argument("-e", "--extra_info", action="store_true", help='Output additional information for each token: SpaceAfter=No if the token was not followed by a space and OriginalSpelling="…" if the token contained whitespace.')
    parser.add_argument("--parallel", type=int, default=1, metavar="N", help="Run N worker processes (up to the number of CPUs) to speed up tokenization.")
    parser.add_argument("--split_sentences", action="store_true", help="Do also split the paragraphs into sentences.")
    parser.add_argument("FILE", type=argparse.FileType("r"), help="The input file")
    args = parser.parse_args()
    return args


def get_paragraphs(fh):
    """Generator for the paragraphs in the file."""
    paragraph = []
    for line in fh:
        if line.strip() == "":
            if len(paragraph) > 0:
                yield "".join(paragraph)
                paragraph = []
        else:
            paragraph.append(line)
    if len(paragraph) > 0:
        yield "".join(paragraph)


def main():
    args = arguments()
    n_tokens = 0
    t0 = time.perf_counter()
    tokenizer = Tokenizer(args.split_camel_case, args.token_classes, args.extra_info)
    sentence_splitter = SentenceSplitter(args.token_classes or args.extra_info)
    if args.paragraph_separator == "empty_lines":
        paragraphs = get_paragraphs(args.FILE)
    elif args.paragraph_separator == "single_newlines":
        paragraphs = (line for line in args.FILE if line.strip() != "")
    if args.parallel > 1:
        pool = multiprocessing.Pool(min(args.parallel, multiprocessing.cpu_count()))
        tokenized_paragraphs = pool.imap(tokenizer.tokenize, paragraphs, 250)
    else:
        tokenized_paragraphs = map(tokenizer.tokenize, paragraphs)
    tokenized_paragraphs = (tp for tp in tokenized_paragraphs if tp)
    if args.split_sentences:
        tokenized_paragraphs = map(sentence_splitter.split, tokenized_paragraphs)
        tokenized_paragraphs = (s for tp in tokenized_paragraphs for s in tp)
    if args.token_classes or args.extra_info:
        tokenized_paragraphs = (["\t".join(t) for t in tp] for tp in tokenized_paragraphs)
    for tp in tokenized_paragraphs:
        n_tokens += len(tp)
        print("\n".join(tp), "\n", sep="")
    t1 = time.perf_counter()
    logging.info("Tokenized %d tokens in %d seconds (%d tokens/s)" % (n_tokens, t1 - t0, n_tokens / (t1 - t0)))
