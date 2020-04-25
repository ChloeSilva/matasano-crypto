from crypto3 import xorCipher

file = open('crypto4.txt', 'r')
bestScore = 10000
bestCode = bytes()
codes = []

for line in file.readlines():
    codes.append(xorCipher(bytes.fromhex(line.strip())))

for code in codes:
    if code[1] < bestScore:
        bestCode = code[0]
        bestScore = code[1]


print('Best score: '+str(bestScore))
print('Likely Answer: '+bestCode.decode('ascii'))