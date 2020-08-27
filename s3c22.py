#!/usr/bin/env python3

from s3c21 import MT19937
import time
from random import randint

class Crack_MT19937:

    def get_output(self):
        seed = int(time.time()) + randint(40, 1000)
        rnd = MT19937(seed)
        return seed, rnd.extract_number() 

    def crack_seed(self, output):
        guess = int(time.time()) + 1000
        rnd = MT19937(guess)
        while rnd.extract_number() != output:
            guess -= 1
            rnd = MT19937(guess)
        return guess

    def test(self):
        seed, output = self.get_output()
        cracked_seed = self.crack_seed(output)
        assert seed == cracked_seed
        return cracked_seed

def main():
    attack = Crack_MT19937() 
    print("[*] seed: " + str(attack.test()))

if __name__ == '__main__':
    main()

