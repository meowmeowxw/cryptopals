from Crypto.Cipher import AES
import base64 

def aes_ecb_decrypt(key, ct):
    ct = base64.b64decode(ct.encode())
    aes = AES.new(key, AES.MODE_ECB)
    return aes.decrypt(ct)

def main():
    key = b'YELLOW SUBMARINE'
    with open("./s1f07.txt", "r") as f:
        ct = f.read()
    pt = aes_ecb_decrypt(key, ct)
    print(pt.decode())

if __name__ == '__main__':
    main()

