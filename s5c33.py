#!/usr/bin/env python3

from os import urandom
from Crypto.Util.number import bytes_to_long, long_to_bytes

class DH:
    
    def __init__(self, p, g, a = None, b = None):
        self.p = p
        self.g = g
        if a == None:
            self.a = self.generate_random()
        else:
            self.a = a
        if b == None:
            self.b = self.generate_random()
        else:
            self.b = b
        self.A = self.pow_mod(self.g, self.a)
        self.B = self.pow_mod(self.g, self.b)
        self.sa = self.pow_mod(self.B, self.a)
        self.sb = self.pow_mod(self.A, self.b)
        
    def generate_random(self):
        x = bytes_to_long(urandom(len(long_to_bytes(self.p)))) % self.p
        while x == 0:
            x = bytes_to_long(urandom(len(long_to_bytes(self.p)))) % self.p
        return x
    
    def pow_mod(self, g, x):
        return pow(g, x, self.p)

def main():
    print("[*]---------------------------------[*]")
    print("[*] Test 1 [*]")
    p = 37
    g = 5
    dh = DH(p, g)
    assert dh.sa == dh.sb
    print(dh.sa)
    print("[*]---------------------------------[*]")
    print("[*] Test 2 [*]")
    p = int('''ffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024
       e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd
       3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec
       6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f
       24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361
       c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552
       bb9ed529077096966d670c354e4abc9804f1746c08ca237327fff
       fffffffffffff'''.replace('\n','').replace(' ', ''), 16)
    g = 2
    dh = DH(p, g)
    assert dh.sa == dh.sb
    print(dh.sa)

if __name__ == '__main__':
    main()

