import string

printable_chars = bytes(string.printable, 'ascii')
encoded = '1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736'
expected = [0.0812, 0.0149, 0.0271, 0.0432, 0.012, 0.0230, 0.0203, 0.0592, 0.0731, 0.0010, 0.0069, 0.0398, 0.0261, 0.0695, 0.0768, 0.0182, 0.0011, 0.0602, 0.0628, 0.0910, 0.0288, 0.0111, 0.0209, 0.0017, 0.0211, 0.0007]

def xorCipher(encoded):
    bestScore = 100
    bestCode = bytes()
    bestKey = 0

    for i in range(0, 128):
        decoded = bytes(x ^ i for x in encoded)
        try:
            if chiSquared(decoded) < bestScore:
                bestScore = chiSquared(decoded)
                bestCode = decoded
                bestKey = i
        except:
            pass

    return(bestCode,bestScore,bestKey)

def chiSquared(byteString):
    badChars = len(list(filter(lambda x: (x not in printable_chars), byteString)))
    asciiString = byteString.decode('ascii')
    decoded = ''.join(filter(lambda x: (x >= 'A') & (x <= 'Z'), str.upper(asciiString)))
    alphaPercentage = (len(decoded)+asciiString.count(' '))/len(byteString)
    actual = []

    if len(decoded) != 0:
        for i in range(65, 91):
            actual.append(len(list(filter(lambda x: x == chr(i), decoded)))/len(decoded))
        return (sum([(y-x)*(y-x)/x for x,y in zip(expected, actual)])+(badChars*10))/(alphaPercentage*10)
    else:
        return 100

if __name__ == "__main__":
    print(xorCipher(bytes.fromhex(encoded))[0].decode('ascii'))