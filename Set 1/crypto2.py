x = '1c0111001f010100061a024b53535009181c'
y = '686974207468652062756c6c277320657965'

def XOR(x, y):
    return bytearray(x_ ^ y_ for x_, y_ in zip(x, y))

print(XOR(bytes.fromhex(x), bytes.fromhex(y)).hex())