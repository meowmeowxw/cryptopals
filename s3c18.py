#!/usr/bin/env python3

import mycrypto as mc
from os import urandom
from struct import pack, unpack
from Crypto.Cipher import AES

class CTR:

    def __init__(self, key):
        self.blocksize = 16
        self.key = key
        self.aes = AES.new(self.key, AES.MODE_ECB)
    
    def encrypt(self, nonce, plaintext):
        counter = 0
        block = plaintext[counter:(counter * self.blocksize) + self.blocksize]
        iv = pack("<QQ", nonce, counter)
        ciphertext = iv
        while block:
            ciphertext += mc.xor(self.aes.encrypt(iv), block) 
            counter += 1
            iv = pack("<QQ", nonce, counter)
            block = plaintext[counter * self.blocksize:\
                    (counter * self.blocksize) + self.blocksize]
        return ciphertext

    def decrypt(self, ciphertext):
        iv = ciphertext[:self.blocksize]
        nonce, _ = unpack("<QQ", iv) 
        return self.encrypt(nonce,
                ciphertext[self.blocksize:])[self.blocksize:]

def main():
    ctr = CTR(urandom(16))
    pt = b'a' * 7 + b'c' * 13
    assert(ctr.decrypt(ctr.encrypt(0, pt))) == pt

if __name__ == '__main__':
    main()
