import curses
from base64 import b64decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from random import randint
import math as m
import string

#Global key variable
key, XORkey, lines, sortedScore = b'', [], [], []

#XOR function
def xor(a,b):
    return list(x^y for x,y in zip(a, b))

#Generates a key and iv for encryptor to use
def generateKey():
    global key
    key = bytes(randint(0,255) for _ in range(0,16))

#CRT encryptor
def encrypt(data):
    global key

    stream = bytearray('', 'ascii')
    for i in range(m.ceil(len(data)/16)):
        stream +=  bytes(8)+(i).to_bytes(8, 'little')

    backend = default_backend()
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=backend)
    encryptor = cipher.encryptor()
    encryptedStream = encryptor.update(stream) + encryptor.finalize()

    return xor(data, encryptedStream)

# Assings a value of likelyhood for a decrypted string
def chiSquared(byteString):
    printable_chars = bytes(string.printable, 'ascii')
    expected = [0.0812, 0.0149, 0.0271, 0.0432, 0.012, 0.0230, 0.0203, 0.0592, 0.0731, 0.0010, 0.0069, 0.0398, 0.0261, 0.0695, 0.0768, 0.0182, 0.0011, 0.0602, 0.0628, 0.0910, 0.0288, 0.0111, 0.0209, 0.0017, 0.0211, 0.0007]

    #badChars = len([x not in printable_chars for x in byteString])
    badChars = len(list(filter(lambda x: (x not in printable_chars), byteString)))
    asciiString = ''.join(list(chr(x) if x in printable_chars else '' for x in byteString))
    decoded = ''.join(filter(lambda x: (x >= 'A') & (x <= 'Z'), str.upper(asciiString)))
    alphaPercentage = (len(decoded)+asciiString.count(' '))/len(byteString)
    actual = []

    if len(decoded) != 0:
        for i in range(65, 91):
            actual.append(len(list(filter(lambda x: x == chr(i), decoded)))/len(decoded))
        return (sum([(y-x)*(y-x)/x for x,y in zip(expected, actual)])+(badChars*10))/(alphaPercentage*10)
    else:
        return 1000

def generateDecryptionKeys(maximum):
    global sortedScore

    # Transpose lines
    xorlines = [b'']*maximum
    for i in range(len(lines)):
        for j in range(len(lines[i])):
            xorlines[j] += bytes([lines[i][j]])
    
    # Rank single xor decryption with chi squared testing
    score = [[] for x in range(maximum)]
    for i in range(len(xorlines)):
        for j in range(256):
            score[i].append(chiSquared(bytes(x ^ j for x in xorlines[i])))

    for char in range(maximum):
        sortedScore.append([i for x,i in sorted([(x,i) for i,x in enumerate(score[char])])])


def initiate(screen, key):
    screen.clear()
    screen.addstr("Manual XOR Decryptor\n\n")

    for line in lines:
        for char in line:
            screen.addstr('*')
        screen.addstr('\n')

    screen.addstr("\nKey:\n")   
    for char in key:
        screen.addstr(str(char)+' ')
    screen.move(1,0)
    
def refresh(screen, key, direction, index):
    screen.clear()
    screen.addstr("Manual XOR Decryptor\n\n")

    end = False
    while(not end):
        if key[index] == 0 and direction == -1:
            key[index] = 0
        elif key[index] == 255 and direction == 1:
            key[index] = 0
        else:
            key[index] = key[index] + direction

        xorlines = []
        sortedScorekey = [sorted[key] for sorted,key in zip(sortedScore,key)]
        for line in lines:
            xorlines.append(xor(line, sortedScorekey))
        
        #for i in range(len(xorlines)):
        try:
            if all(chr(xorlines[i][index]) in string.printable[:95] for i in range(len(xorlines))):
                end = True
        except IndexError:
            end = True

    for line in xorlines:
        for char in line:
            if chr(char) in string.printable[:95]:
                screen.addstr(chr(char))
            else:
                screen.addstr('*')
        screen.addstr('\n')

    screen.addstr("\nKey:\n")
    sortedScorekey = [sorted[key] for sorted,key in zip(sortedScore,key)] 
    for char in sortedScorekey:
        screen.addstr(str(char)+' ')

    return key

def main(stdscr):
    global lines
    # Read input
    with open("crypto19.txt", 'r') as f:
        lines = f.readlines()
    
    # Encrypt input
    maximum = 0
    generateKey()
    for i in range(len(lines)):
        lines[i] = encrypt(b64decode(lines[i]))
        if len(lines[i]) > maximum: maximum = len(lines[i])
    generateDecryptionKeys(maximum)

    # Set up key array
    i = 0
    key = [0]*maximum
    mode = "mode: quick" 
    initiate(stdscr, key)

    while True:
        c = stdscr.getch()
        if c == curses.KEY_UP:
            key = refresh(stdscr, key, 1, i)
            stdscr.move(1,i)
        elif c == curses.KEY_DOWN:
            key = refresh(stdscr, key, (-1), i)
            stdscr.move(1,i)
        elif c == curses.KEY_LEFT:
            if i != 0:
                i -= 1
                stdscr.move(1,i)
        elif c == curses.KEY_RIGHT:
            if i < (maximum-1):
                i += 1
                stdscr.move(1,i)
        elif c == 27:
            break

curses.wrapper(main)