#!/usr/bin/env python3

import time

class MT19937:

    W, N, M, R = 32, 624, 397, 31
    A = 0x9908b0df
    U, D = 11, 0xffffffff
    S, B = 7, 0x9d2c5680
    T, C = 15, 0xefc60000
    L = 18
    F = 1812433253
    
    def __init__(self, seed):
        self.LOWER_MASK = (1 << self.R) - 1
        self.UPPER_MASK = self.lowest_bit(not self.LOWER_MASK, self.W)
        self.MT = [i for i in range(self.N)]
        self.index = self.N
        self.seed_MT(seed)

    def lowest_bit(self, a, n):
        mask = (1 << n) - 1
        return a & mask

    def seed_MT(self, seed):
        self.MT[0] = seed
        for i in range(1, self.N):
            first = self.MT[i - 1]
            second = self.MT[i - 1] >> (self.W - 2) 
            self.MT[i] = self.lowest_bit(self.F * (first ^ second) + i, self.W)
    
    def extract_number(self):
        if self.index >= self.N:
            if self.index > self.N:
                print("generator was never seeded")
            # Permute state every 624 outputs to achieve
            # period of 2**19937
            self.twist()
        y = self.MT[self.index]
        y = y ^ ((y >> self.U) & self.D)
        y = y ^ ((y << self.S) & self.B)
        y = y ^ ((y << self.T) & self.C)
        y = y ^ (y >> self.L)
        self.index = self.index + 1
        return self.lowest_bit(y, self.W)
    
    def twist(self):
        for i in range(self.N):
            x = (self.MT[i] & self.UPPER_MASK) +\
                    (self.MT[(i + 1) % self.N] & self.LOWER_MASK)
            xA = x >> 1
            if (x % 2) != 0:
                xA = xA ^ self.A
            self.MT[i] = self.MT[(i + self.M) % self.N] ^ xA
        self.index = 0

def main():
    print("[*]----------------------[*]")
    mt = MT19937(39324)
    for _ in range(5):
        print(mt.extract_number())
    print("[*]----------------------[*]")

if __name__ == '__main__':
    main()
