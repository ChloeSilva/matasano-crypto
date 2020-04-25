#CTR encryption
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from base64 import b64decode
from math import ceil

#XOR function
def xor(a,b):
    return bytearray(x^y for x,y in zip(a, b))

#CRT encryptor
def encrypt(data, nonce):
    stream = bytearray('', 'ascii')
    for i in range(ceil(len(data)/16)):
        stream +=  nonce+(i).to_bytes(8, 'little')

    key = b'YELLOW SUBMARINE'
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()
    encryptedStream = encryptor.update(stream) + encryptor.finalize()

    return xor(data, encryptedStream)


#CTR decryptor
def decrypt(data, nonce):
    stream = bytearray('', 'ascii')
    for i in range(ceil(len(data))):
        stream += nonce+(i).to_bytes(8, 'little')

    key = b'YELLOW SUBMARINE'
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    decryptor = cipher.encryptor()
    decryptedStream = decryptor.update(stream) + decryptor.finalize()

    return xor(data, decryptedStream)

if __name__ == "__main__":
    encoded = "L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ=="
    print(decrypt(b64decode(encoded), bytes(8)).decode('ascii'))
    encrypted = encrypt(b'Hey cutie', bytes(8))
    print(decrypt(encrypted,bytes(8)).decode('ascii'))