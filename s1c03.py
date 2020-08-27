#!/usr/bin/env python3

import numpy as np
import mycrypto as mc

englishLetterFreq = {
        ' ': 0.1918182,
        'e': 0.1041442,
        't': 0.0729357,
        'a': 0.0651738,
        'o': 0.0596302,
        'i': 0.0558094,
        'n': 0.0564513,
        's': 0.0515760,
        'r': 0.0497563,
        'h': 0.0492888,
        'd': 0.0349835,
        'l': 0.0331490,
        'u': 0.0225134,
        'c': 0.0217339,
        'm': 0.0202124,
        'f': 0.0197881,
        'w': 0.0171272,
        'g': 0.0158610,
        'y': 0.0145984,
        'p': 0.0137645,
        'b': 0.0124248,
        'v': 0.0082903,
        'k': 0.0050529,
        'x': 0.0013692,
        'q': 0.0008606,
        'j': 0.0009033,
        'z': 0.0007836,
        }

def english_score(str):
    score = 0
    for s in str:
        # return 0 in case the key doesn't exist
        score += englishLetterFreq.get(chr(s).lower(), 0)
    return score

def solve_xor_frequency(s):
    max_freq = 0
    for x in range(0, 256):
        x = bytes([x])
        res = mc.single_xor(x, s)
        freq = english_score(res)
        if freq > max_freq:
            max_freq = freq
            key = x
    return (max_freq, key, mc.single_xor(key, s))

def main():
    s = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
    freqmax, key, res = solve_xor_frequency(bytes.fromhex(s))
    print(str(res) + "\t freq: " + str(freqmax) + "\t key: " + str(key))

if __name__ == '__main__':
    main()

"""
Cheat method lol 
for x in range(0, 256):
    x = bytes([x])
    res = mc.xor_string(x * len(bytes.fromhex(s)), bytes.fromhex(s))
    try:
        if (mc.isreadable(res.decode())):
            counter = collections.Counter(res)
        else:
            continue
    except UnicodeDecodeError:
        continue
"""

