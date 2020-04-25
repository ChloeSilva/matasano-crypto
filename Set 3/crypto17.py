#The CBC padding oracle
#Uses padding validation to break CBC ciphers
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from random import randint
from base64 import b64decode

#Global key and iv variables
key, iv = b'',b''

#Generates a key and iv for encryptor to use
def generateKey():
    global key
    key = bytes(randint(0,255) for _ in range(0,16))  

#Pads a given bytes object to PKCS7
def padPKCS(data, blocksize):
    size = blocksize - len(data) % blocksize if len(data) % blocksize else blocksize
    return data+(size*bytes([size]))

#Unpads PKCS7, raises exception if padding is invalid
def unpadPKCS(data):
    size = data[-1]
    if not all(x == size for x in data[-size:-1]):
        raise RuntimeError('Bad padding')
    else:
        return data[0:-size]

#Selects random line and encrypts it
def encrypt():
    global key, iv

    #Generates initialisation vector
    iv = bytes(randint(0,255) for _ in range(0,16))

    #Selects a random line
    with open('crypto17.txt','r') as f:
        lines = f.readlines()
    data = b64decode(lines[randint(0,9)])

    #Pads and encrypts line
    data = padPKCS(data, 16)
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(data) + encryptor.finalize()

    return bytearray(encrypted)

#Decrypts AES and checks padding validity
def decrypt(encrypted):
    global key, iv

    #Decrypts data
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(encrypted) + decryptor.finalize()

    #Check padding
    try:
        decrypted = unpadPKCS(decrypted)
    except:
        return False
    else:
        return True

#Cracks CBC encryption using padding oracle
def crack(encrypted):
    global iv

    encrypted = iv+encrypted
    decrypted = bytearray('', 'ascii')
    for block in reversed(range(int(len(encrypted)/16))):
        chunk = bytearray(0 for _ in range(16))
        if block == 0: break
        for byte in reversed(range(16)):
            for char in range(0,255):
                chunk[byte] = char
                before = bytes(x^y for x,y in zip(chunk, bytes(16*[16-byte])))
                if decrypt(before+encrypted[(block)*16:(block+1)*16]):
                    decrypted.insert(0, (encrypted[(block-1)*16+byte] ^ char))
                    break

    return unpadPKCS(decrypted).decode('ascii')

generateKey()
print(crack(encrypt()))