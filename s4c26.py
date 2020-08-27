#!/usr/bin/env python3

from s3c18 import CTR
from os import urandom
from Crypto.Cipher import AES
from Crypto.Util.number import bytes_to_long as bl
from mycrypto import xor

class Oracle:
    
    def __init__(self):
        self.blocksize = AES.block_size
        self.key = urandom(self.blocksize)
        self.ctr = CTR(self.key)
        self.prefix = b'comment1=cooking%20MCs;userdata='
        self.suffix = b';comment2=%20like%20a%20pound%20of%20bacon'
    
    def encrypt(self, data):
        plaintext = self.prefix
        plaintext += data.replace(b';', b'?').replace(b'=', b'?')
        plaintext += self.suffix
        nonce = bl(urandom(self.blocksize // 2))
        return self.ctr.encrypt(nonce, plaintext)

    def decrypt(self, ciphertext):
        plaintext = self.ctr.decrypt(ciphertext)
        return b';admin=true;' in plaintext

class CTR_Bit_Flip:

    def __init__(self):
        self.oracle = Oracle()
        self.semi_colon = bytes([ord(';')])
        self.equal = bytes([ord('=')])
    
    def attack(self): 
        message = b'\x00admin\x00true\x00'
        ciphertext = bytearray(self.oracle.encrypt(message))
        ciphertext[48] = bl(xor(bytes([ciphertext[48]]), self.semi_colon))
        ciphertext[48 + 6] = bl(xor(bytes([ciphertext[48 + 6]]), self.equal))
        ciphertext[48 + 11] = \
                bl(xor(bytes([ciphertext[48 + 11]]), self.semi_colon))
        return self.oracle.decrypt(ciphertext)

def main():
    ctr_bit_flip = CTR_Bit_Flip()
    if ctr_bit_flip.attack() == True:
        print("[*] attack successful")
        print("[*] injected: ;admin=true;") 
    else:
        print("[*] attack failed")
        exit(1)

if __name__ == '__main__':
    main()

