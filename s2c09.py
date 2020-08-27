import mycrypto as mc

def main():
    s = b'YELLOW SUBMARINE'
    pad = mc.PKCS7(20)
    res = pad.encode(s)
    print(res)

if __name__ == '__main__':
    main()
