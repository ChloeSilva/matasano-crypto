def unpadPKCS(data):
    size = data[-1]
    if not all(x == size for x in data[-size:-1]):
        raise RuntimeError('Bad padding')
    else:
        return data[0:-size]