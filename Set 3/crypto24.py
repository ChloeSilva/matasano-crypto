import crypto21
from os import urandom
from random import randint
import time

encryptionSeed = 0

# Encrypt/Decrypts data using the MT19937 stream cipher
def MT_stream_cipher(data, seed):
    crypto21.initialise_MT(seed)

    # Generate keystream
    keystream = bytearray('', 'ascii')
    for _ in range(len(data)):
        keystream += bytes([crypto21.mersenne_twister()%256])

    # Returns xor of keystream and data
    return bytes(x ^ y for x, y in zip(data, keystream))

# Encrypts data using the MT stream cipher using a random 16 bit seed
# after prepending a random number of random bytes
def encrypt(data):
    global encryptionSeed
    encryptionSeed = randint(0,2**16-1)
    prefix = bytes(randint(0,255) for _ in range(randint(5,30)))
    message = prefix + data

    return MT_stream_cipher(message, encryptionSeed)

# Finds the seed of a given stream cipher (Brute force)
def crack():
    input = b'Bubble_kid'
    encrypted = encrypt(input)

    for i in range(2**16):
        decrypted = MT_stream_cipher(encrypted, i)
        if decrypted[-(len(input)):] == input:
            return i

# Generates a password reset token using MT based on the current time
def generate_password_token():
    crypto21.initialise_MT(int(time.time()))
    return crypto21.mersenne_twister()

# Checks if a password token is still valid for the current time
def validate_password_token(token, timeValid):
    currentTime = int(time.time())
    for seed in range(currentTime-timeValid,currentTime):
        crypto21.initialise_MT(seed)
        rand = crypto21.mersenne_twister()
        if token == rand: 
            return True
    
    return False

if __name__ == "__main__":

    #Brute force MT19937 stream cipher
    assert(crack() == encryptionSeed)
    print("identified seed: ",crack())

    #Initialise and check password reset token
    token = generate_password_token()
    time.sleep(5)
    assert(not validate_password_token(token, 2))
    assert(validate_password_token(token, 7))
