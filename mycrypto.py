import binascii
import re

class PKCS7(): 

    def __init__(self, blocksize):
        self.blocksize = blocksize

    def encode(self, s):
        padding = self.blocksize - (len(s) % self.blocksize) 
        if padding == 0 :
            return s
        else:
            return s + (padding * (chr(padding)).encode())

    def decode(self, s):
        return s[:-(s[-1])]
    
    def check(self, s):
        padding = s[-s[-1]:]
        return all(padding[b] == len(padding) for b in range(0, len(padding)))

#    def check(self, s):
#        last = ord(s[-1:].decode())
#        if last > self.blocksize:
#            raise ValueError('bad padding')
#        s = s[::-1]
#        for i in range(0, last):
#            if s[i] != last:
#                raise ValueError('bad pad')
#        return True
#
def string_to_hex(s):
    return s.encode().hex()

def hex_to_string(s):
    return bytes.fromhex(s).decode()

def single_xor(s1, s2):
    return xor_string(s1 * len(s2), s2)

def multi_xor(s1, s2):
    return xor_string(s1 * (len(s2) // len(s1) + 1), s2)

def xor_string(s1, s2):
    if(len(s1) == 1 and len(s2) == 1):
        return bytes([ord(s1) ^ ord(s2)])
    else:
        return bytes(x ^ y for x, y in zip(s1, s2))

def xor(s1, s2):
    return xor_string(s1, s2)

def isreadable(str): # check if contains normal text characters
    return bool(re.search('^[a-zA-Z0-9\., \'\"\-_\:\(\)]+$', str)) 

def english_score(str):
    score = 0
    for s in str:
        # when we iterate a byte string s --> int
        # return 0 in case the key doesn't exist
        score += english_letter_freq.get(chr(s).lower(), 0)
    return score

def solve_xor_frequency(s):
    max_freq = 0
    key = b''
    for x in range(0, 256):
        x = bytes([x])
        res = single_xor(x, s)
        freq = english_score(res)
        if freq > max_freq:
            max_freq = freq
            key = x
    return key

def transpose(ct, blocksize):
    transposed = [b'' for _ in range(0, blocksize)]
    for i in range(0, blocksize):
        for j in range(i, len(ct), blocksize):
            transposed[i] += bytes([ct[j]])
    """
    transposed = b''
    for i in range(0, blocksize):
        for j in range(i, len(ct), blocksize):
            transposed += bytes([ct[j]])
    return [transposed[i:i + blocksize] \
            for i in range(0, len(transposed), blocksize)]
    """
    return transposed

def hamming(s1, s2):
    assert len(s1) == len(s2)
    distance = 0
    for b1, b2 in zip(s1, s2):
        # When using zip normal conversion to int
        # xor is possible between two int
        res = b1 ^ b2  
        # convert to bin and count "1" 
        distance += bin(res).count("1")
        # alternative way using gmpy2 (faster)
        # distance += popcount(mpz(res)) which uses sse cpu ;)
    return distance

def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modular_sqrt(a, p):
# https://gist.githubusercontent.com/nakov/60d62bdf4067ea72b7832ce9f71ae079/raw/\
# \864c0eb6e58329db8444a7a6fc3df28c0fc8580f/modsqrt.py
    def legendre_symbol(a, p):
        ls = pow(a, (p - 1) // 2, p)
        return -1 if ls == p - 1 else ls

    # Simple cases
    if legendre_symbol(a, p) != 1:
        return 0
    elif a == 0:
        return 0
    elif p == 2:
        return p
    elif p % 4 == 3:
        return pow(a, (p + 1) // 4, p)

    s = p - 1
    e = 0
    while s % 2 == 0:
        s //= 2
        e += 1
    
    n = 2
    while legendre_symbol(n, p) != -1:
        n += 1
    
    x = pow(a, (s + 1) // 2, p)
    b = pow(a, s, p)
    g = pow(n, s, p)
    r = e

    while True:
        t = b
        m = 0
        for m in range(r):
            if t == 1:
                break
            t = pow(t, 2, p)

        if m == 0:
            return x

        gs = pow(g, 2 ** (r - m - 1), p)
        g = (gs * gs) % p
        x = (x * gs) % p
        b = (b * g) % p
        r = m

def identify_ecb(ct):
    bsize = 16
    blocks = [ct[i: i + bsize] for i in range(0, len(ct), bsize)]
    for i in range(0, len(blocks)):
        for j in range(i+1, len(blocks)-1):
            if blocks[i] == blocks[j]:
                return True
    return False

english_letter_freq = {
        ' ': 0.1918182,
        'e': 0.1041442,
        't': 0.0729357,
        'a': 0.0651738,
        'o': 0.0596302,
        'i': 0.0558094,
        'n': 0.0564513,
        's': 0.0515760,
        'r': 0.0497563,
        'h': 0.0492888,
        'd': 0.0349835,
        'l': 0.0331490,
        'u': 0.0225134,
        'c': 0.0217339,
        'm': 0.0202124,
        'f': 0.0197881,
        'w': 0.0171272,
        'g': 0.0158610,
        'y': 0.0145984,
        'p': 0.0137645,
        'b': 0.0124248,
        'v': 0.0082903,
        'k': 0.0050529,
        'x': 0.0013692,
        'q': 0.0008606,
        'j': 0.0009033,
        'z': 0.0007836,
        }

