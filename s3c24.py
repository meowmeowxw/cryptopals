#!/usr/bin/env python3

from s3c21 import MT19937
from mycrypto import xor
from Crypto.Util.number import bytes_to_long
from os import urandom

class MT_STREAM:

    def __init__(self, seed):
        self.prng = MT19937(seed)

    def encrypt(self, plaintext, seed = None):
        ciphertext = b''
        if seed is not None:
            self.prng = MT19937(seed)
        for p in plaintext:
            key = bytes([self.prng.extract_number() % 256])
            ciphertext += xor(key, bytes([p]))
        return ciphertext

    def decrypt(self, ciphertext, seed = None):
        return self.encrypt(ciphertext, seed)

class Oracle:

    def __init__(self, seed):
        self.enc = MT_STREAM(seed)

    def encrypt(self, plaintext):
        return self.enc.encrypt(plaintext)

def main():
    seed = bytes_to_long(urandom(2))
    enc = MT_STREAM(seed)
    pt = b'a' * 10
    assert enc.decrypt(enc.encrypt(pt), seed) == pt

if __name__ == '__main__':
    main()

