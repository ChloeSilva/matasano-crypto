import crypto21
import time

# Constants defined to MT19937 specifications
u, d = 11, 0xFFFFFFFF
s, b = 7, 0x9D2C5680
t, c = 15, 0xEFC60000
l, f = 18, 1812433253

# Untempers a given number to discover the MT generator state
def untemper(x):
    x = x ^ (x >> l)
    x = x ^ ((x << t) & c) 
    for _ in range(7):
        x = x ^ ((x << s) & b)
    for _ in range(3):
        x = x ^ (x >> u)

    return x

# Tempers a number according to MT
def temper(y):
    y = y ^ (y >> u)  
    y = y ^ ((y << s) & b)
    y = y ^ ((y << t) & c)
    y = y ^ (y >> l)

    return y

if __name__ == "__main__":
    tapped = []
    generator = []

    # Initialise MT, and use untempered tapped values to recreate
    # the initial state of the generator
    crypto21.initialise_MT(int(time.time()))
    for i in range(624):
        tapped.append(crypto21.mersenne_twister())
        generator.append(untemper(tapped[i]))

    print("first tapped value:   ", tapped[0])
    print("first predicted value:", temper(generator[0]))
