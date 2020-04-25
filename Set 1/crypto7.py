from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

messageb64 = open('crypto7.txt').read()
message = base64.b64decode(messageb64)
open('input.data', 'wb').write(message)
key = str.encode("YELLOW SUBMARINE")

backend = default_backend()
cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
encryptor = cipher.encryptor()
decryptor = cipher.decryptor()
messageDecrypted = decryptor.update(message) + decryptor.finalize()
print(messageDecrypted.decode('ascii'))