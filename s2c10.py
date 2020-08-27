from Crypto.Cipher import AES
import mycrypto as mc
import base64

class CBC:

    def __init__(self, key, bsize):
        self.key = key
        self.bsize = bsize
        self.aes = AES.new(self.key, AES.MODE_ECB)

    def encrypt(self, iv, plaintext):
        # Pad the plaintext
        pad = mc.PKCS7(self.bsize)
        plaintext = pad.encode(plaintext)
        # Final ciphertext 
        ciphertext = b''
        # Blocks of ciphertext
        ctblocks = []
        # Blocks of plaintext 
        ptblocks = [plaintext[i:i + self.bsize] \
                for i in range(0, len(plaintext), self.bsize)]

        # CBC Encryption
        for i in range(0, len(ptblocks)):
            if i == 0:
                ctblocks.append(self.aes.encrypt(mc.xor_string(ptblocks[i], iv)))
            else:
                ctblocks.append(self.aes.encrypt(mc.xor_string(ptblocks[i], ctblocks[i - 1])))
            ciphertext += ctblocks[i]
        
        # Return
        return iv + ciphertext

    def decrypt(self, ciphertext):
        # Final plaintext
        plaintext = b''
        # Blocks of ciphertext
        ctblocks = [ciphertext[i:i + self.bsize] for i in range(0, len(ciphertext), self.bsize)]

        # CBC Decryption
        for i in range(1, len(ctblocks)):
            plaintext += mc.xor_string(ctblocks[i - 1], self.aes.decrypt(ctblocks[i]))
        
        # Unpad and return
        pad = mc.PKCS7(self.bsize)
        try:
            if pad.check(plaintext) == True:
                return pad.decode(plaintext)
        except ValueError:
            return False
def main():
    # Values taken from coursera cryptography I
    key = bytes.fromhex('140b41b22a29beb4061bda66b6747e14')
    ciphertext = bytes.fromhex('4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81')
    blocksize = 16 
    cbc = CBC(key, blocksize)
    # Test enc(dec(ct)) == ct
    plaintext = cbc.decrypt(ciphertext)
    assert ciphertext == cbc.encrypt(ciphertext[:blocksize], plaintext)

    # Cryptopals part
    key = b'YELLOW SUBMARINE'
    with open("./s2f10.txt", "r") as f:
        ciphertext = base64.b64decode(f.read())
    
    cbc = CBC(key, blocksize)
    # cbc.decrypt(ciphertext.decode())
    print(cbc.decrypt(ciphertext))

if __name__ == '__main__':
    main()

