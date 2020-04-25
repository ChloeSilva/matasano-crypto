from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from random import randint

def encrypt(input):
    before = bytes(randint(0,128) for _ in range(0,randint(5,10)))
    after = bytes(randint(0,128) for _ in range(0,randint(5,10)))
    data = before+input+after
    mode = randint(0,1)
    key = bytes(randint(0,128) for _ in range(0,16))
    backend = default_backend()

    size = 16 - len(data) % 16 if len(data) % 16 else 16
    data = data+(size*bytes([0]))

    if mode:
        cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    else:
        iv = bytes(randint(0,128) for _ in range(0,16))
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=backend)

    encryptor = cipher.encryptor()
    encrypted = encryptor.update(data) + encryptor.finalize()

    print("Encrypting in ECB") if mode else print("Encrypting in CBC")
    return encrypted

def identify():
    encrypted = encrypt(100*bytes([0]))
    print("Identified: ECB") if encrypted[26:42] == encrypted[42:58] else print("Identified: CBC")

identify()
