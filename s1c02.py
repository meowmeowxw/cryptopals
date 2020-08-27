#!/usr/bin/env python3

import mycrypto as mc

def xor(s1, s2):
    return mc.xor_string(bytes.fromhex(s1), bytes.fromhex(s2))

def main():
    s1 = '1c0111001f010100061a024b53535009181c'
    s2 = '686974207468652062756c6c277320657965'
    res = xor(s1, s2)
    assert res.hex() == '746865206b696420646f6e277420706c6179'

if __name__ == '__main__':
    main()
