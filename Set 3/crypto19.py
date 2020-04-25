import curses
from base64 import b64decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from random import randint
import math as m
import string

#Global key variable
key, XORkey, lines = b'', [], []

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
            key[index] = 255
        elif key[index] == 255 and direction == 1:
            key[index] = 0
        else:
            key[index] = key[index] + direction

        xorlines = []
        for line in lines:
            xorlines.append(xor(line, key))
        
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
    for char in key:
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