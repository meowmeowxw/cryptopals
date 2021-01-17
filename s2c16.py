#!/usr/bin/env python3

from os import urandom, path
from s2c10 import CBC
from colorama import Fore, Style
from mycrypto import xor

class Oracle:
    
    def __init__(self):
        self.blocksize = 16
        self.key = urandom(self.blocksize)
        self.cbc = CBC(self.key, self.blocksize)
        self.prefix = 'comment1=cooking%20MCs;userdata='
        self.suffix = ';comment2=%20like%20a%20pound%20of%20bacon'

    def encrypt(self, data):
        plaintext = self.prefix
        plaintext += data.replace(';', '?').replace('=', '?')
        plaintext += self.suffix
        iv = urandom(self.blocksize)
        return self.cbc.encrypt(iv, plaintext.encode())

    def decrypt(self, ciphertext):
        return self.cbc.decrypt(ciphertext)

class CBC_Bit_Flip:

    def __init__(self, oracle, charlist, debug):
        self.oracle = oracle
        self.charlist = charlist
        self.debug = debug

    def get_bsize(self):
        plaintext = ''
        initial_len = len(self.oracle.encrypt(plaintext))
        final_len = initial_len
        while final_len == initial_len:
            plaintext += 'a'
            final_len = len(self.oracle.encrypt(plaintext)) 
        return (final_len - initial_len)

    def get_prefix(self):
        # Find equal length of two different cipertexts
        ct1 = self.oracle.encrypt('a')
        ct2 = self.oracle.encrypt('b')
        return len(path.commonprefix([ct1, ct2]))
    
    def xor_table(self):
        dict = {}
        for c in self.charlist:
            dict[c] = chr(ord(c) ^ 1)
        return dict

    def attack(self, injection, block):
        bsize = self.get_bsize()
        # Not work when IV is randomized
        equal_length = self.get_prefix()
        # payload[:16] will be decrypted in garbage
        payload = 'a' * (bsize * 2)
        if self.debug:
            print(Fore.YELLOW + "[*] Dictionary : " + str(dict))
            print(Fore.YELLOW + "[*] Payload : " + str(payload))
            print(Fore.YELLOW + "[*] Blocksize : " + str(bsize))
            print(Fore.YELLOW + "[*] Equal length : " + str(equal_length))
        # p_{i+1} xor 'a' * 16 xor ;admin = true;bbbb 
        # p_{i+1} = ;admin=true;bbbb
        ciphertext = list(self.oracle.encrypt(payload))
        ct = ciphertext[(bsize * block):(bsize * (block + 1))]
        xored = list(xor(xor(bytes(ct), b'a' * bsize), injection))
        ciphertext[(bsize * block):(bsize * (block + 1))] = xored
        return bytes(ciphertext)

def main():
    charlist = [';', '=']
    injection = b';admin=true;bbbb'
    oracle = Oracle()
    cbc_bit_flip = CBC_Bit_Flip(oracle, charlist, True)
    # equal_length = cbc_bit_flip.get_prefix()
    # When iv is fixed 
    # ciphertext = cbc_bit_flip.attack(injection, int(equal_length / 16))
    # When iv is random
    ciphertext = cbc_bit_flip.attack(injection, 3)
    print(Fore.CYAN + "[*] Ciphertext : " + str(ciphertext))
    print(Fore.GREEN + "[*] Decrypted ciphertext : " + 
            str(oracle.decrypt(ciphertext)))
    if b';admin=true;' in oracle.decrypt(ciphertext):
        print(Fore.MAGENTA + "[*] Attack completed")
    else:
        print(Fore.RED + "[:(] Attack unsuccessful")
        exit(1)

if __name__ == '__main__':
    main()

