#!/usr/bin/env python3

import base64

def decode(s):
    b64 = base64.b64encode(bytes.fromhex(s))
    return b64.decode()

def main():
    s = ("49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f6973"
        "6f6e6f7573206d757368726f6f6d")
    assert(decode(s) == ("SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3Vz"
                        "IG11c2hyb29t"))

if __name__ == '__main__':
    main()

