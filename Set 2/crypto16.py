from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from random import randint

key, iv = b'', b''

def generateKey():
    global key, iv
    key = bytes(randint(0,128) for _ in range(0,16))
    iv = bytes(randint(0,128) for _ in range(0,16))

def padPKCS(data, blocksize):
    size = blocksize - len(data) % blocksize if len(data) % blocksize else blocksize
    return data+(size*bytes([size]))

def unpadPKCS(data):
    size = data[-1]
    if not all(x == size for x in data[-size:-1]):
        raise RuntimeError('Bad padding')
    else:
        return data[0:-size]

def encrypt(input):
    global key, iv

    before = "comment1=cooking%20MCs;userdata="
    after = ";comment2=%20like%20a%20pound%20of%20bacon"
    input = input.replace(";", "").replace("=","")

    message = padPKCS(str.encode(before+input+after), 16)
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(message) + encryptor.finalize()

    return encrypted

def isAdmin(encrypted):
    global key

    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(encrypted) + decryptor.finalize()
    decrypted = unpadPKCS(decrypted)

    return b';admin=true;' in decrypted

def makeAdmin():
    encrypted = bytearray(encrypt('true'))
    encrypted[9:15] = [x ^ ord(y) ^ ord(z) for x,y,z in zip(encrypted[9:15],';admin','erdata')]
    return encrypted

generateKey()
print(isAdmin(makeAdmin()))