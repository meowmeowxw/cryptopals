#!/usr/bin/env python3

from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
from os import urandom
from mycrypto import PKCS7
from s1c08 import identify_ecb
import base64

key = urandom(16)
blocksize = 16

def oracle(plaintext):
    string = base64.b64decode('Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIG'\
            'Rvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IH'\
            'dhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZH'\
            'JvdmUgYnkK'.encode())
    pad = PKCS7(blocksize)
    aes = AES.new(key, AES.MODE_ECB)
    return aes.encrypt(pad.encode(plaintext + string))

def get_bsize():
    plaintext = b''
    # aes-ecb(key, unknown-string || pad)
    initial_len = len(oracle(plaintext))
    final_len = initial_len
    # aes-ecb(key, plaintext || unknown-string || pad)
    while final_len == initial_len:
        plaintext += b'a'
        final_len = len(oracle(plaintext)) 

    return (final_len - initial_len)

def get_secret(part_secret):
    # Length of plaintext must be between 0 and 15, so % blocksize = 16
    length_plaintext = (blocksize - (1 + len(part_secret))) % blocksize
    # Length to crack is always length_plaintext + len(secret that I know) + 1
    # After the first block has been decrypted, we need to reconstruct the 
    # length_plaintext to 15, and add to it during the verification (if) 
    # the part_secret 
    length_to_crack = length_plaintext + len(part_secret) + 1
    # Create plaintext
    plaintext = b'a' * length_plaintext
    # Ciphertext to compare
    ciphertext = oracle(plaintext)[:length_to_crack] 
    # Let's try all values
    for x in range(0, 256):
        x = bytes([x])
        if ciphertext == oracle(plaintext + part_secret + x)[:length_to_crack]:
            return x
    return b''

def main():
    # blocksize = get_bsize() --> 16, easier to set this as global variable
    test_ecb = b'a' * 100
    a, b = identify_ecb(oracle(test_ecb))
    assert a is not None and b is not None

    ciphertext_crack = oracle(b'')
    part_secret = b''
    for i in range(len(ciphertext_crack)):
        part_secret += get_secret(part_secret)
    
    pad = PKCS7(blocksize)
    print("[*] Plaintext : " + str(pad.decode(part_secret)))

if __name__ == '__main__':
    main()
