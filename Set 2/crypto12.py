from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
from random import randint
import itertools

key = b''

def generateEncryption():
    global key
    key = bytes(randint(0,128) for _ in range(0,16))

def encrypt(input):
    global key
    with open('crypto12.txt','r') as f:
        message = base64.b64decode(f.read())
    
    data = input+message
    paddedData = data+((16-len(data)%16)*bytes([0]))

    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(paddedData) + encryptor.finalize()

    return encrypted

def decryptAESECB(encryptor):
    #Determine block size:
    bsize = 16
    for i in range(2,128):
        if encryptor(i*b'A')[0:i] == encryptor((i+1)*b'A')[0:i]:
            bsize = i
            print('Block size: '+str(i))
            break

    #Detect ECB:
    if encryptor(bsize*2*b'A')[0:bsize] == encryptor(bsize*2*b'A')[bsize:2*bsize]:
        print("Identified: ECB")
    else:
        print("Unknown encryption method")

    #Byte-at-a-time attack
    decrypted = b''
    for i in range(0,int(len(encryptor(b'')))):
        start = int(i/bsize)*bsize
        end = (int(i/bsize)+1)*bsize
        input = (bsize-(i%bsize+1))*b'A'
        for char in range(0,128):
            if encryptor(input)[start:end] == encryptor(input+decrypted+bytes([char]))[start:end]:
                decrypted += bytes([char])
                break

    return decrypted

if __name__ == "__main__":
    generateEncryption()
    print(decryptAESECB(encrypt).decode('ascii'))