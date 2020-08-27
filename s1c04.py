#!/usr/bin/env python3

from s1c03 import englishLetterFreq, solve_xor_frequency
import mycrypto as mc

def main():
    lines = [bytes.fromhex(line.rstrip('\n')) \
            for line in open("./s1f04.txt", "r")]

    plaintexts = []
    for s in lines:
        plaintexts.append(solve_xor_frequency(s))
    print(max(plaintexts)[2])

if __name__ == '__main__':
    main()

