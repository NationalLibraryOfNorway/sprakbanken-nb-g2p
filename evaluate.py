#!/usr/bin/env python
# coding=utf-8

#%%
import re, sys, os
from collections import defaultdict

import Levenshtein
from pathlib import Path


def load_tsv_dict(filename: str) -> list:
    """Read a tab separated dictionary file to a list of lists:

    Args:
        filename (str): text file in this format:
            overlast	OA2 V AX0 RL AH3 S T
            tankegymnastikks	T AH2 NG K AX0 G YH0 M N AH0 S T IH3 K S
            vasallene	V AH0 S AH1 L NX0 AX0
    Returns:
        list: format [word, transcription]
    """
    return [line.split("\t") for line in Path(filename).read_text().splitlines()]

def load_pronlex(refs_file: str) -> dict:
    """Read a tab separated dictionary file to a dict of words and phonemes:

    Args:
        filename (str): text file in this format:
            overlast	OA2 V AX0 RL AH3 S T
            tankegymnastikks	T AH2 NG K AX0 G YH0 M N AH0 S T IH3 K S
            vasallene	V AH0 S AH1 L NX0 AX0
    Returns:
        dict: {"word": ["transcription"]}
    """
    refs = {}

    with open (refs_file, "r", encoding="utf-8") as ifp:
        for line in ifp:
            parts = re.split('\t', line.strip())
            word = parts.pop(0)
            refs [word] = parts.split(" ")
            #refs [word] = parts

    return refs

#%%
def phoneme_error_rate(p_seq1, p_seq2):
    """Source: https://fehiepsi.github.io/blog/grapheme-to-phoneme/"""
    p_vocab = set(p_seq1 + p_seq2)
    p2c = dict(zip(p_vocab, range(len(p_vocab))))
    c_seq1 = [chr(p2c[p]) for p in p_seq1]
    c_seq2 = [chr(p2c[p]) for p in p_seq2]
    return Levenshtein.distance(''.join(c_seq1),
                                ''.join(c_seq2)) / len(c_seq2)
#%%
def g2pstats(gold, test):
    """Source: https://github.com/Sprakbanken/g2p-nb/blob/master/g2p_stats.py"""

    total_w = len(gold)
    total_p = sum([len(v) for v in gold.values])
    print(total_p)
    test_per = 0
    test_wer = 0
    for word, testtrans in test.items:
        #testtrans = item.strip().split('\t')[-1].split(' ')
        #goldtrans = gold[n].strip().split('\t')[-1].split(' ')
        #testtrans = trans
        goldtrans = gold[word]
        per = phoneme_error_rate(testtrans, goldtrans)
        wer = int(testtrans != goldtrans)
        test_per += per
        test_wer += wer
    #test_per = test_per / total_p * 100
    #test_wer = test_wer / total_w * 100
#    print(f'| WER | PER |')
#    print(f'| --- | --- |')
#    print(f'| {test_wer} | {test_per} |')
    return total_w, total_p, test_wer, test_per

#%%
def print_stats(total_w, total_p, test_w, test_p):

    test_per = test_per / total * 100
    test_wer = test_wer / total * 100
    print(f'| WER | PER |')
    print(f'| --- | --- |')
    print(f'| {test_wer} | {test_per} |')


def evaluate(reference_file, predicted_file):

    test = load_pronlex(predicted_file)
    gold = load_pronlex(reference_file)

    if not len(test) == len(gold):
        sys.exit('test and gold file do not have the same length')
    print_stats(*g2pstats(gold, test))


#%%
if __name__ == "__main__":
    import argparse

    example = "{0} --lexicon e_written".format (sys.argv [0])
    parser = argparse.ArgumentParser (description=example)
    parser.add_argument ("--lexicon", "-l", help="Lexicon dialect variant.",
                         default="e_written")
    parser.add_argument ("--lexicon", "-l", help="Lexicon dialect variant.",
                         default="e_written")

    args = parser.parse_args ()
    lexicon = args.lexicon

    #%%

    reference_file = f"reference_data/NB-uttale_{lexicon}_test.dict"
    predicted_file = f"predicted_data/predicted_nb_{lexicon}.dict"

    #%%
    #compute_eval(reference_file, predicted_file)
    #%%
    evaluate(reference_file, predicted_file)


# %%
