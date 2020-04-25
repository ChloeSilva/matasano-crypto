with open("crypto8.txt", 'r') as f:
    data = [bytes.fromhex(line.strip()) for line in f.readlines()]

def detectECB(data):
    for line in data:
        chunks = [line[i*16:(i+1)*16] for i in range(0, int(len(line)/16))]
        if len(chunks) != len(set(chunks)):
            return line

    return b'No dected ECB'

print(detectECB(data))