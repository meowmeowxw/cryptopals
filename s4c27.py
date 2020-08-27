#!/usr/bin/env python3

from mycrypto import xor
from s2c10 import CBC
from os import urandom
from Crypto.Cipher import AES

class Oracle:

    def __init__(self):
        self.key = urandom(16)
        self.cbc = CBC(self.key, AES.block_size)

    def encrypt(self, plaintext):
        print("[*] key oracle: " + str(self.key))
        if len(plaintext) < (AES.block_size * 2):
            return None
        ciphertext = self.cbc.encrypt(self.key, plaintext)
        return ciphertext[AES.block_size:], ciphertext[:AES.block_size]
                
    def decrypt(self, iv, ciphertext):
        return self.cbc.decrypt(iv + ciphertext)
        
def attack(ciphertext):
    blocks = [ciphertext[i:i + AES.block_size] \
            for i in range(0, len(ciphertext), AES.block_size)]
    blocks[1] = b'\x00' * AES.block_size
    blocks[2] = blocks[0]
    return b''.join([b for b in blocks])

def main():
   message = ("comment1=cooking%20MCs;userdata="
              "comment2=%20like%20a%20pound%20of%20bacon").encode()
   oracle = Oracle()
   ciphertext, iv = oracle.encrypt(message)
   ciphertext_tampered = attack(ciphertext)
   plaintext = oracle.decrypt(iv, ciphertext_tampered) 
   blocks = [plaintext[i:i + AES.block_size] \
           for i in range(0, len(plaintext), AES.block_size)]
   cracked_key = xor(blocks[0], blocks[2])
   assert oracle.key == cracked_key
   print("[*] cracked key: " + str(cracked_key))

if __name__ == '__main__':
    main()

