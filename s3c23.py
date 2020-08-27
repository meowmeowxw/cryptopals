#!/usr/bin/env python3

from s3c21 import MT19937

def undo_right(y):
    return y

def undo_left(y):
    return y

def undo_xor_right(y):
    """
    l = 18
    z = y ^ (y >> l)
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx    y
                                        xor
    000000000000000000xxxxxxxxxxxxxx    y >> l
                                        =
    xxxxxxxxxxxxxxxxxx??????????????    z
                                        xor
    000000000000000000xxxxxxxxxxxxxx    z >> l
                                        =
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx    y
    """
    return (y ^ (y >> MT19937.L))

def undo_left_xor_and(y):
    """
    t = 15, c = 0xefc60000 = 11101111110001100000000000000000 
    z = y ^ ((y << t) & c)
    xxxxxxxxxxxxxxx00000000000000000    y << T
                                        and
    11101111110001100000000000000000    C
                                        =
    ???????????????00000000000000000    intermediate-step 
                                        xor
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx    y
                                        =
    !!!!!!!!!!!!!!!xxxxxxxxxxxxxxxxx    z


    xxxxxxxxxxxxxxx00000000000000000    z << T
                                        and
    11101111110001100000000000000000    C
                                        =
    ???????????????00000000000000000    intermediate-step 
                                        xor
    !!!!!!!!!!!!!!!xxxxxxxxxxxxxxxxx    z
                                        =
    xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx    y
    """
    return (y ^ ((y << MT19937.T) & MT19937.C))

def untemper(y):
    y = undo_xor_right(y) 
    y = undo_left_xor_and(y)
    # f(y) = y ^ ((y << S) & B)
    # If the function f is applied 7 times it returns y
    # I don't know why
    for _ in range(7):
        y ^= y << MT19937.S & MT19937.B
    # The same with f(y) = y ^ ((y >> U) & D)
    for _ in range(3):
        y ^= y >> MT19937.U
    return y

def clone_mt(mt):
    mt_clone = MT19937(0)
    for i in range(624):
        mt_clone.MT[i] = untemper(mt.extract_number())
    return mt_clone

def main():
    mt = MT19937(5489)
    mt_clone = clone_mt(mt)
    for _ in range(2000):
        assert mt_clone.extract_number() == mt.extract_number()

if __name__ == '__main__':
    main()

