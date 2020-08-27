#!/usr/bin/env python3

from s1c03 import solve_xor_frequency
import numpy as np
import base64
from itertools import combinations
import mycrypto as mc

def hamming(s1, s2):
    assert len(s1) == len(s2)
    distance = 0
    for b1, b2 in zip(s1, s2):
        # When using zip normal conversion to int
        # xor is possible between two int
        res = b1 ^ b2  
        # convert to bin and count "1" 
        distance += bin(res).count("1")
        # alternative way using gmpy2 (faster)
        # distance += popcount(mpz(res)) which uses sse cpu ;)
    return distance

def compute_keysizes(ct):
    distances = {0 : 0 for i in range(0, 41)}
    # (1)
    for ksize in range(2, 41):
        # takes 4 blocks as suggested
        blocks = [ct[i:i + ksize] for i in range(0, 4 * ksize, ksize)]
        # construct a pair of all possible combinations 
        pairs = combinations(blocks, 2)
        distance = 0
        # compute hamming distance of every pair and 
        # to compute the average we need to dived for 6
        # because 6 = 3! (all possible combinations)
        for (x, y) in pairs:
            # (2)
            distance += hamming(x, y) 
        distance /= 6
        # normalize distance
        # (3 - 4)
        distance /= ksize
        distances[ksize] = distance

    # Sort the dictionary and take the 5 lower values (short distance hamming)
    # Start from 1 because there's a (0, 0) in the beginning
    sorted_d = sorted(distances.items(), key = lambda distances:distances[1])[1:6]
    # initialize list with possible keysize 
    keysizes = [sorted_d[i][0] for i in range(0, len(sorted_d))]
    return keysizes

def compute_key(ct, keysizes):
    keys = [b'' for i in range(0,len(keysizes))]
    index = 0
    for ksize in keysizes:
        blocks = [ct[i:i + ksize] for i in range(0, len(ct), ksize)]
        transpose = [b'' for i in range(0, len(blocks[0]))]
        for i in range(0, len(blocks[0])):
            for j in range(0, len(blocks)):
                try :
                    transpose[i] += bytes([blocks[j][i]])
                except IndexError:
                    continue
        for t in transpose:
            keys[index] += solve_xor_frequency(t)[1]
        index += 1
    print("[*] possible keys\n" + str(keys) + "\n\n")
    return keys

def try_keys(ct, keys):
    for key in keys:
        res = mc.xor_string(key * len(ct), ct)
        try:
            print(res.decode())
        except UnicodeDecodeError:
            continue
       
def main():
    # Test 
    s1 = b'this is a test'
    s2 = b'wokka wokka!!!'
    assert hamming(s1, s2) == 37

    # Read base64 file and decode it in ct (ciphertext)
    with open("./s1f06.txt", "r") as f:
        content = f.read()
    ct = base64.b64decode(content.encode())

    # Solve
    keysizes = compute_keysizes(ct)
    keys = compute_key(ct, keysizes)
    try_keys(ct, keys)
     
if __name__ == '__main__':
    main()
