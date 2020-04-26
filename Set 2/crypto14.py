from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64
from random import randint
import itertools

key,before = b'',b''

def generateEncryption():
    global key,before
    key = bytes(randint(0,128) for _ in range(0,16))
    before = bytes(randint(0,128) for _ in range(0,randint(0,100)))

def encrypt(input):
    global key,before
    with open('crypto12.txt','r') as f:
        message = base64.b64decode(f.read())
    
    data = before+input+message
    paddedData = data+((16-len(data)%16)*bytes([0]))

    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(paddedData) + encryptor.finalize()

    return encrypted

def decryptAESECB():
    #Determine block size:
    blocksize = 2
    while True:
        encrypted = encrypt(4*blocksize*b'A')
        split = [encrypted[i*blocksize:(i+1)*blocksize] for i in range(0,int(len(encrypted)/blocksize))]
        if any(split.count(i) == 3 for i in split):
            block = list(filter(lambda x: split.count(x) == 3, split))[0]
            break
        else:
            blocksize += 1
    print("Block size: "+str(blocksize))

    #Detect ECB:
    encrypted = encrypt(((blocksize*3)+100)*b'A')
    if encrypted[100:100+blocksize] == encrypted[100+blocksize:100+(2*blocksize)]:
        print("Identified: ECB")
    else:
        print("Unknown encryption method")

    #Detect amount of prepended blocks and bytes
    blocksBefore = encrypt(10*blocksize*b'A').find(block)
    for i in itertools.count():
        if block in encrypt((i+blocksize)*b'A'):
            bytesBefore = i
            break

    #Byte-at-a-time attack
    decrypted = b''
    for char in range(1,len(encrypt(b''))):
        start = blocksBefore+blocksize*(int(char/16))
        end = blocksBefore+blocksize*(1+int(char/16))
        padding = (bytesBefore+blocksize-(char%blocksize))*b'A'
        for i in range(0,128):
            if encrypt(padding)[start:end] == encrypt(padding+decrypted+bytes([i]))[start:end]:
                decrypted += bytes([i])
                break
        
    return decrypted

generateEncryption()
print(decryptAESECB().decode('ascii'))