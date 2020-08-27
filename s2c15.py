#!/usr/bin/env python3

def check_pad(s):
    last = ord(s[-1:].decode())
    s = s[::-1]
    for i in range(0, last):
        if s[i] != last:
            return False
            # raise ValueError('bad pad')
    return True

def main():
    assert check_pad(b'Ice baby\x01\x02\x03\x04') == False
    assert check_pad(b'Ice baby\x04\x04\x04\x04') == True
    assert check_pad(b'Ice baby' + b'\x16' * 14) == False
    assert check_pad(b'Ice baby' + b'\x17' * 17) == False

if __name__ == '__main__':
    main()

