#!/usr/bin/env python3

from struct import pack, unpack
from Crypto.Hash import SHA1 as SHA1_True
import struct

class SHA1:

    def __init__(self, data, state = None, length = None):
        self.data = data
        if state is None:
            self.H = [
                0x67452301,
                0xefcdab89,
                0x98badcfe,
                0x10325476,
                0xc3d2e1f0
            ]
        else:
            self.H = state
        self.length = length 

    __MASK = 0xffffffff

    @staticmethod
    def __ROTL(shift, value, max = 32):
        return (((value << shift) & SHA1.__MASK) | (value >> (max - shift)))

    def glue_padding(self):
        # Compute length in bits
        # append the bit '1' to the message --> by adding 0x80 = 0b10000000
        # if message length is a multiple of 8 bits (normally it is :|).
        # append 0 ≤ k < 512 bits '0', such that the resulting message 
        # length in bits is congruent to −64 ≡ 448 (mod 512)
        # We need length in bits
    
        if self.length is None:
            ml = len(self.data) * 8
        else:
            ml = self.length
        self.data += b'\x80'
        while(len(self.data) * 8) % 512 != 448:
            self.data += b'\x00'
        # append ml, the original message length, as a 
        # 64-bit big-endian integer. Thus, the total length is
        # a multiple of 512 bits.
        self.data += pack(">Q", ml)
        return self.data

    def process(self):
        for i in range(0, len(self.data), 64):
            w = []
            for j in range(16):
                w.append(unpack(">I", self.data[i + (j * 4):i + (j * 4) + 4])\
                        [0])
            for j in range(16, 80):
                w.append(self.__ROTL(1, \
                        w[j - 3] ^ w[j - 8] ^ w[j - 14] ^ w[j - 16]))
            a = self.H[0]
            b = self.H[1]
            c = self.H[2]
            d = self.H[3]
            e = self.H[4]

            for j in range(0, 80):
                if 0 <= j <= 19:
                    f = (b & c) | ((~ b) & d)
                    k = 0x5a827999
                elif 20 <= j <= 39:
                    f = b ^ c ^ d
                    k = 0x6ed9eba1
                elif 40 <= j <= 59:
                    f = (b & c) | (b & d) | (c & d)
                    k = 0x8f1bbcdc
                elif 60 <= j <= 79:
                    f = b ^ c ^ d
                    k = 0xca62c1d6
                temp = (SHA1.__ROTL(5, a) + f + e + k + w[j]) & SHA1.__MASK
                e = d
                d = c
                c = SHA1.__ROTL(30, b) & SHA1.__MASK
                b = a
                a = temp

            self.H[0] = (self.H[0] + a) & SHA1.__MASK 
            self.H[1] = (self.H[1] + b) & SHA1.__MASK
            self.H[2] = (self.H[2] + c) & SHA1.__MASK
            self.H[3] = (self.H[3] + d) & SHA1.__MASK
            self.H[4] = (self.H[4] + e) & SHA1.__MASK 
           
    def hexdigest(self):
        self.glue_padding()
        self.process()
        return '%08x%08x%08x%08x%08x' % \
                (self.H[0], self.H[1], self.H[2], self.H[3], self.H[4])
    def digest(self):
        return bytes.fromhex(self.hexdigest())

def main():
    message = b'boi'
    sha1 = SHA1(message)
    md = sha1.digest()
    sha1_true = SHA1_True.new()
    sha1_true.update(message)
    assert md == sha1_true.digest()

if __name__ == '__main__':
    main()

