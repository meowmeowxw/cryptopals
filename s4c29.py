#!/usr/bin/env python3

from s4c28 import SHA1
from struct import pack, unpack
from Crypto.Util.number import long_to_bytes
from random import randint

class SHA1_Length_Extension:

    def __init__(self):
        pass

    def glue_padding(self, message):
        # Compute length in bits
        # append the bit '1' to the message --> by adding 0x80 = 0b10000000
        # if message length is a multiple of 8 bits (normally it is :|).
        # append 0 ≤ k < 512 bits '0', such that the resulting message 
        # length in bits is congruent to −64 ≡ 448 (mod 512)
        # We need length in bits
        bit_len = len(message) * 8 
        message += b'\x80'
        while(len(message) * 8) % 512 != 448:
            message += b'\x00'
        # append ml (bit_len), the original message length, as a 
        # 64-bit big-endian integer. Thus, the total length is
        # a multiple of 512 bits.
        message += pack(">Q", bit_len)
        return message
    
    def get_register(self, hash):
        # sha1 is a 160 bit message digest
        # register 32 bit
        # 160 / 32 = 5 registers
        return list(unpack(">5I", hash))
    
    def attack(self, hash, message, payload, oracle):
        # we want to recreate the state of the sha1 function,
        # to do so we need to guess the length of the key to form
        # the correct padding.
        # after that we ignore the first k bytes and we add the payload.
        # the forged_hash will be always the same because it will be computed
        # over the same state (that we can compute using the hash of a 
        # signed message), while the forged message will be different
        # at every iteration.
        for k in range(100):
            forged = self.glue_padding(b'a' * k + message)[k:] + payload
            ml = (k + len(forged)) * 8
            # the get_register must be done inside the for, or the values
            # will change (list are mutable in python (?))
            r = self.get_register(hash)
            # forged hash will always be the same
            sha1 = SHA1(payload, r, ml)
            forged_hash = sha1.digest()
            if oracle.validate(forged, forged_hash):
                print("[*] attack successful")
                print("[*] forged hash : " + str(forged_hash.hex()))
                print("[*] forged message : " + str(forged))
                return True
        return False

class Oracle:

    def __init__(self):
        self.option = randint(1, 100)
        self.key = b'a' * self.option

    def get_hash(self, message):
        sha1 = SHA1(self.key + message)
        return sha1.digest()

    def validate(self, message, hash):
        sha1 = SHA1(self.key + message)
        return sha1.digest() == hash

def main():
    sha1_length_extension = SHA1_Length_Extension()
    oracle = Oracle()
    message = b'comment1=cooking%20MCs;userdata=foo;'
    message += b'comment2=%20like%20a%20pound%20of%20bacon'
    payload = b';admin=true'
    hash = oracle.get_hash(message) 
    if not sha1_length_extension.attack(hash, message, payload, oracle):
        print("attack didn't work sorry")
        exit(1)

if __name__ == '__main__':
    main()

