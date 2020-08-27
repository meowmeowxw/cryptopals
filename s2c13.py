#!/usr/bin/env python3

import mycrypto as mc
from random import randint
from Crypto.Cipher import AES
from os import urandom

key = urandom(16)

def parse(s):
    dict = {}
    values = s.split('&')
    for v in values:
        v = v.split('=')
        dict[v[0]] = v[1]
    return dict

def encode(dict):
    s = ''
    for d in dict.items():
        s += d[0] + '=' + d[1] + '&'
    # Remove final &
    return s[:-1]

def profile_for(email):
    # Blacklist characters email = email.replace('&', '').replace('=', '') 
    dict = {}
    dict['email'] = email
    dict['uid'] = '10'
    dict['role'] = 'user'
    return encode(dict)

def encrypt_profile_for(email):
    aes = AES.new(key, AES.MODE_ECB)
    pad = mc.PKCS7(16)
    return aes.encrypt(pad.encode(profile_for(email).encode()))

def decrypt_profile(ciphertext):
    aes = AES.new(key, AES.MODE_ECB)
    pad = mc.PKCS7(16)
    profile = aes.decrypt(ciphertext)
    return parse(pad.decode(profile).decode())

def main():
    # Test 1
    print("[*] Test 1")
    dict = parse('foo=bar&baz=qux&zap=zazzle')
    print(dict)
    print(encode(dict))

    # Test 2
    print("\n[*] Test 2")
    print(profile_for('foo@bar.com'))
   
    # Generate a plaintex that encrypted corresponds to role=admin
    # email=a * (16 - len(mail=)) --> email=a*10
    # admin+(pad)
    # &uid=10&role=user
    print("\n[*] ECB Cut-and-Paste")
    email1 = 'a' * 10 + 'admin' + (chr(11) * 11)
    ct1 = encrypt_profile_for(email1)
    # email=giovanni.d isanti+cryptopal sset2@protonmail .com&uid=10&role=
    # user
    email2 = 'giovanni.disanti+cryptopalset2@protonmail.com'
    ct2 = encrypt_profile_for(email2)
    ct = ct2[:(16 * 4)] + ct1[16:32]
    print(decrypt_profile(ct))
    print(
    """
    \n[*] We have created an email with a role = admin
    using an oracle that sets role = user
    """
    )

if __name__ == '__main__':
    main()
