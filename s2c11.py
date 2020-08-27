#!/usr/bin/env python3

from s1c08 import identify_ecb
from s2c10 import CBC
from Crypto.Cipher import AES
from Crypto.Util.number import long_to_bytes
from secrets import randbits, SystemRandom
from mycrypto import PKCS7
from os import urandom

blocksize = 16

# CPA (Chosen Plaintext Attack Y34h)

def oracle_cbc_ecb(plaintext):
    # Generate random key
    key = urandom(16)
    # Alternative way
    # key = long_to_bytes(randbits(128)) --> Error sometimes it generates less bytes
    # Probably long_to_bytes didn't work properly

    # Instance secret_generator
    secrets_generator = SystemRandom()

    # Prepend and append chunk of 5 --> 10 bytes
    chunk = secrets_generator.randint(5, 10)
    plaintext = urandom(chunk) + plaintext
    chunk = secrets_generator.randint(5, 10)
    plaintext += urandom(chunk)

    # Choose to encrypt using CBC or ECB
    option = secrets_generator.randint(0, 1)
    if option == 0:
        cbc = CBC(key, blocksize)
        iv = urandom(16)
        return cbc.encrypt(iv, plaintext)
    else:
        pad = PKCS7(blocksize)
        ecb = AES.new(key, AES.MODE_ECB)
        return ecb.encrypt(pad.encode(plaintext))

def main():
    cbc_counter = 0
    ecb_counter = 0
    for i in range(0, 1000):
        plaintext = b'a' * 100
        a, b = identify_ecb(oracle_cbc_ecb(plaintext))
        if a is not None and b is not None:
            cbc_counter += 1
        else:
            ecb_counter += 1

    print("CBC Encryption : " + str(cbc_counter))
    print("ECB Encryption : " + str(ecb_counter))

if __name__ == '__main__':
    main()
