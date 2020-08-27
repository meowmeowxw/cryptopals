#!/usr/bin/env python3

import mycrypto as mc

def main():
    s = ("Burning 'em, if you ain't quick and nimble\n"
            "I go crazy when I hear a cymbal")
    key = "ICE"
    res = mc.xor_string(key.encode() * (len(s) // len(key) + 1), s.encode())
    assert res.hex() == ("0b3637272a2b2e63622c2e69692a23693a2a3c6324202d623d63"
            "343c2a26226324272765272a282b2f20430a652e2c652a3124333a653e2b20276"
            "30c692b20283165286326302e27282f")

if __name__ == '__main__':
    main()

