# Constants defined to MT19937 specifications
w, n, m, r = 32, 624, 397, 31
a = 0x9908B0DF
u, d = 11, 0xFFFFFFFF
s, b = 7, 0x9D2C5680
t, c = 15, 0xEFC60000
l, f = 18, 1812433253
MT = list(range(n))
lower_mask = 0x7FFFFFFF
upper_mask = 0x80000000
index = n+1

#
def initialise_MT(seed):
    global index
    index = n
    MT[0] = seed
    for i in range(1,n):
        MT[i] = d & (f * (MT[i-1] ^ (MT[i-1] >> (w-2))) + i)

def twist():
    global index
    
    for i in range(n):
        x = (MT[i] & upper_mask) + (MT[(i+1)%n] & lower_mask)
        xA = x >> 1
        if x%2 != 0: xA = xA ^ a
        MT[i] = MT[(i+m)%n] ^ xA

    index = 0

def mersenne_twister():
    global index
    if index >= n: 
        if index > n: initialise_MT(5489)
        twist()

    y = MT[index]
    y = y ^ (y >> u)  
    y = y ^ ((y << s) & b)
    y = y ^ ((y << t) & c)
    y = y ^ (y >> l)

    index = index + 1
    return d & y