from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from itertools import takewhile
from random import randint
import crypto12

key = b''

def generateKey():
    global key
    key = bytes(randint(0,128) for _ in range(0,16))

def parse(string):
    answer = '{\n'
    for i in [x.split('=') for x in string.split('&')]:
        answer += "  "+i[0]+": '"+i[1]+"',\n"
    return answer[0:-2]+"\n}"

def profileFor(email):
    email = email.replace('&','')
    email = email.replace('=','')
    return parse("email="+email+"&uid=1&role=user")

def encrypt(email):
    global key
    profile = str.encode(profileFor(email))
    profile = profile+((16-len(profile)%16)*bytes([0]))
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()
    encrypted = encryptor.update(profile) + encryptor.finalize()
    return encrypted

def decrypt(input):
    global key
    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    decryptor = cipher.decryptor()
    decrypted = decryptor.update(input) + decryptor.finalize()
    return decrypted

def makeAdmin():
    root = encrypt('cs@gmail.com')[0:48]
    end = encrypt("aaaaadmin'\n}\x00\x00\x00\x00\x00\x00\x00\x00")[16:32]
    return root+end

generateKey()
print(decrypt(makeAdmin()).decode('ascii'))