#!/usr/bin/env python3

from s3c18 import CTR
from os import urandom
from base64 import b64decode
from mycrypto import xor, solve_xor_frequency

def read_file(path):
    return [line.rstrip('\n') for line in open(path)]

def encrypt(lines):
    ctr = CTR(urandom(16))
    return [ctr.encrypt(0, b64decode(l.encode()))[16:] for l in lines]

def crack_key_ctr(ciphertexts):
    cracked_key = b''
    for i in range(max([len(c) for c in ciphertexts])):
        block = b''
        for c in ciphertexts:
            if i < len(c):
                block += bytes([c[i]])
        cracked_key += solve_xor_frequency(block)
    return cracked_key

def main():
    lines = read_file('./s3f19.txt')
    ciphertexts = encrypt(lines)
    cracked_key = crack_key_ctr(ciphertexts)
    print("[*] key: " + str(cracked_key))
    for c in ciphertexts:
        print(xor(cracked_key, c))

if __name__ == '__main__':
    main()
