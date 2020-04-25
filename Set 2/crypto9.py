def padPKCS(data, blocksize):
    size = blocksize - len(data) % blocksize if len(data) % blocksize else blocksize
    return data+(size*bytes([size]))