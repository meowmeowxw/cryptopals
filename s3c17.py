#!/usr/bin/env python3

from mycrypto import PKCS7, xor
from os import urandom
from random import randint
from s2c10 import CBC
from base64 import b64decode
import sys

class Oracle:

    def __init__(self):
        self.blocksize = 16
        self.key = urandom(self.blocksize)
        self.cbc = CBC(self.key, self.blocksize)
        self.option = randint(0, 9)
        self.lines = [line.rstrip('\n') for line in open("./s3f17.txt")]

    def encrypt(self):
        iv = urandom(self.blocksize)
        plaintext = b64decode(self.lines[self.option].encode())
        return self.cbc.encrypt(iv, plaintext)

    def decrypt(self, ciphertext):
        result = self.cbc.decrypt(ciphertext)
        return result is not None

class CBC_Padding_Oracle:

    def __init__(self):
        self.chars = self.get_chars()
        self.oracle = Oracle()
        self.ciphertext = self.oracle.encrypt()
        self.blocks = [self.ciphertext[i:i + self.oracle.blocksize] for i in
                range(0, len(self.ciphertext), self.oracle.blocksize)]

    def get_chars(self):
        chars = []
        for i in range(0x61, 0x7f):
            chars.append(bytes([i]))
        for i in range(0x41, 0x61):
            chars.append(bytes([i]))
        for i in range(0x20, 0x41):
            chars.append(bytes([i]))
        for i in range(0x1f, 0x00 - 1, -1):
            chars.append(bytes([i]))
        for i in range(0x7f, 0xff + 1):
            chars.append(bytes([i]))
        return chars
            
    def create_pad(self, n):
        return n * chr(n).encode()
    
    def create_payload(self, ct, pad, char):
        p = xor(xor(ct[-len(pad):], pad), char)
        return ct[:-len(pad)] + p
    
    def attack(self, log):
        msg = b''
        for i in range(0, len(self.blocks) - 1):
            if log == True:
                print("Decrypting Block : " + str(i + 1))
            pt = b''
            plaintext = b''
            for j in range(1, len(self.blocks[i]) + 1):
                for k in self.chars:
                    pad = self.create_pad(j)
                    pt = k + pt
                    payload = self.create_payload(self.blocks[i], pad, pt)
                    res = self.oracle.decrypt(payload + self.blocks[i + 1])
                    if res == True:
                        plaintext = pt
                        break
                    else:
                        pt = plaintext
            if log == True:
                print("plaintext for block " + str(i + 1) + " : " +\
                        str(plaintext))
            msg += plaintext
        return msg

def main():
    cbc_padding_oracle = CBC_Padding_Oracle()
    msg = cbc_padding_oracle.attack(True)
    print("message decrypted : " + str(msg))

if __name__ == '__main__':
    main()

