from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

messageb64 = open('crypto10.txt').read()
message = base64.b64decode(messageb64)
key = str.encode("YELLOW SUBMARINE")

backend = default_backend()
cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)

def xor(x,y):
    return bytes(x_ ^ y_ for x_, y_ in zip(x, y))

def CBC(data):
    chunks = [data[i*16:(i+1)*16] for i in range(0, int(len(data)/16))]
    chunks.insert(0,bytes([0])*16)
    decrypted = []

    for i in range(0,len(chunks)):
        decryptor = cipher.decryptor()
        x = decryptor.update(chunks[i]) + decryptor.finalize()
        decrypted.append(xor(x, chunks[i-1]))
    
    return b''.join(decrypted[1:])

print(CBC(message).decode('ascii'))