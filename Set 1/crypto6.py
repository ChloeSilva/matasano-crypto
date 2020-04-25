import itertools as it
import math as m
from crypto3 import xorCipher
import codecs

def xor(string, key):
    return bytes(x ^ y for x,y in zip(string, key*len(string)))

def hamming(pair):
    x = bin(int.from_bytes(pair[0], 'big'))
    y = bin(int.from_bytes(pair[1], 'big'))
    counter = 0
    for a,b in zip(x,y):
        if a != b:
            counter += 1
    return counter

def keySize(code):
    scores = []
    minKeySize = 2
    maxKeySize = 40

    for keySize in range(minKeySize,maxKeySize):
        scores.append(hamming((code[0:keySize],code[keySize:2*keySize]))/keySize)
    
    scores = list(zip(scores,list(range(2,maxKeySize))))
    scores.sort()
    return (scores[0][1],scores[1][1],scores[2][1])

def keyValue(code, keySize):
    blocks = [[] for _ in range(keySize)]
    for i in range(0,keySize):
        extra = 1 if i < len(code) % keySize else 0
        for j in range(0,m.floor(len(code)/keySize)+extra):
            blocks[i].append(code[j*keySize+i])
    
    key = (list(xorCipher(x)[2] for x in blocks))
    score = sum(xorCipher(x)[1] for x in blocks)/keySize
    
    return (score,key)

file = open('crypto6.txt', 'r')
code = codecs.decode(str.encode(file.read()), 'base64')
print(xor(code,str.encode('Terminator X: Bring the noise')).decode('ascii'))