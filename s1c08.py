#!/usr/bin/env python3

def identify_ecb(ct):
    bsize = 16
    blocks = [ct[i: i + bsize] for i in range(0, len(ct), bsize)]
    for i in range(0, len(blocks)):
        for j in range(i+1, len(blocks)-1):
            if blocks[i] == blocks[j]:
                return (ct, blocks[i])
    return (None, None)

def main():
    lines = [bytes.fromhex(line.rstrip('\n')) for line in open("./s1f08.txt", "r")]
    for ct in lines:
        ciphertext, block = identify_ecb(ct)
        if ciphertext is not None and block is not None:
            print("ciphertext : " + str(ciphertext.hex()))
            print("block : " + str(block.hex()))

if __name__ == '__main__':
    main()
