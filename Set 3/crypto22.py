import crypto21
import time
from random import randint

# Generates a random number using Unix timestamp as seed
def generate_random():
    time.sleep(randint(40,100))
    seed = int(time.time())
    crypto21.initialise_MT(seed)
    time.sleep(randint(40,100))
    return crypto21.mersenne_twister()

# Finds a seed given the first number generated (rand)
# and an upper and lower bound for the seed (a,b)
def find_seed(a, b, rand):
    for i in range(a,b):
        crypto21.initialise_MT(i)
        if crypto21.mersenne_twister() == rand:
            return i

if __name__ == "__main__":
    before = int(time.time())
    rand = generate_random()
    after = int(time.time())

    print(find_seed(before, after, rand))