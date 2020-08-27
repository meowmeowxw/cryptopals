#!/usr/bin/env python3

from s3c18 import CTR
from os import urandom
from struct import pack, unpack
from mycrypto import xor
from Crypto.Util.number import bytes_to_long
from Crypto.Cipher import AES

def read_file():
    lines = [line.rstrip('\n') for line in open('./s4f25.txt', 'r')]
    return (''.join(lines)).encode()

class Oracle:

    def __init__(self):
        self.key = urandom(16)
        self.nonce = bytes_to_long(urandom(8))
        self.aes = AES.new(self.key, AES.MODE_ECB)
        self.ctr = CTR(self.key)
        self.blocksize = AES.block_size
        
    def encrypt(self, plaintext):
        self.plaintext = plaintext
        return self.ctr.encrypt(self.nonce, plaintext)
    
    def gen_keystream(self, ciphertext, offset, length_plaintext):
        keystream = b''
        nonce, counter = unpack("<QQ", ciphertext)
        counter = offset // self.blocksize 
        max_counter = (length_plaintext + offset) // self.blocksize
        for i in range(counter, max_counter + 1):
            keystream += self.aes.encrypt(pack("<QQ", nonce, i))    

    def edit(self, ciphertext, key, offset, new_text):
        edited_plaintext = self.plaintext[:offset]
        edited_plaintext += new_text
        edited_plaintext += self.plaintext[offset + len(new_text):]
        return self.ctr.encrypt(self.nonce, edited_plaintext)

def main():
    pt = read_file()
    print(pt)
    oracle = Oracle()
    ct = oracle.encrypt(pt)
    ct_edited = oracle.edit(ct, oracle.key, 50, b'porcobio')
    print(ct_edited)

if __name__ == '__main__':
    main()

