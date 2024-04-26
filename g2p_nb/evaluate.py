#!/usr/bin/env python
# coding=utf-8

# %%
import re, sys, os
from collections import defaultdict

import Levenshtein
from pathlib import Path


def load_pronlex(filename: str) -> dict:
    """Read a tab separated dictionary file to a dict of words and phonemes:

    Args:
        filename (str): text file in this format:
                overlast	OA2 V AX0 RL AH3 S T
                tankegymnastikks	T AH2 NG K AX0 G YH0 M N AH0 S T IH3 K S
            or with a score:
                vasallene	13.56   V AH0 S AH1 L NX0 AX0
    Returns:
        dict: {"word": "transcription"}
    """
    pronlex = {}

    for line in Path(filename).read_text().splitlines():
        parts = re.split('\t', line.strip())
        word = parts.pop(0)
        pronlex [word] = parts.pop()  # the transcription is always last
    return pronlex


def phoneme_error_rate(p_seq1, p_seq2):
    """Source: https://fehiepsi.github.io/blog/grapheme-to-phoneme/
    """
    p_vocab = set(p_seq1 + p_seq2)
    p2c = dict(zip(p_vocab, range(len(p_vocab))))
    c_seq1 = [chr(p2c[p]) for p in p_seq1]
    c_seq2 = [chr(p2c[p]) for p in p_seq2]
    errors = Levenshtein.distance(''.join(c_seq1),''.join(c_seq2))  # Count of mismatching tokens
    rate = errors / len(c_seq2)
    return rate


def word_error_rate(w1: str, w2: str) -> int:
    """Return 1 for mismatching strings, 0 for identical strings"""
    return int(w1 != w2)


def evaluate(predicted_file, reference_file):
    """
    Adjusted to account for different transcription lengths,
    so PER is calculated as the sum of phoneme errors divided by sum of all phonemes.
    """
    test = load_pronlex(predicted_file)
    gold = load_pronlex(reference_file)

    phone_errors = 0
    word_errors = 0
    total_phones = 0

    for word, prediction in test.items():
        reference = gold[word]
        refsplit = reference.split(" ")
        reflen = len(refsplit)
        total_phones += reflen

        phone_errors += reflen*phoneme_error_rate(prediction.split(" "), refsplit)
        word_errors += word_error_rate(prediction, reference)

    total_words  = len(test)
    per = phone_errors / total_phones * 100
    wer = word_errors / total_words * 100
    return wer, per


# %%
if __name__ == "__main__":
    # %%
    import argparse

    lexica = [
        "e_written",
        "e_spoken",
        "sw_written",
        "sw_spoken",
        "w_written",
        "w_spoken",
        "t_written",
        "t_spoken",
        "n_written",
        "n_spoken",
    ]
    example = "{0} --lexicon e_written".format (sys.argv [0])
    parser = argparse.ArgumentParser (description=example)
    parser.add_argument(
        "--lexicon",
        "-l",
        help="Lexicon pronunciation variant, with a letter for the dialect area (e, w, sw, t, n) and a style (written, spoken).",
        default=lexica,
        nargs="*",
    )
    args = parser.parse_args ()

    print(f"| Model | Word Error Rate | Phoneme Error Rate |")
    print(f'| --- | --- | --- |')

    for lexicon in args.lexicon:
        reference_file = f"data/NB-uttale_{lexicon}_test.dict"
        predicted_file = f"data/predicted_nb_{lexicon}.dict"
        wer, per = evaluate(predicted_file, reference_file)
        print(f'| *nb_{lexicon}.fst* | {wer} | {per} |')
