def rotr(x, n):
    return ((x >> n) | (x << (32 - n))) & 0xffffffff

def ch(x, y, z):
    return (x & y) ^ ((~x) & z)

def maj(x, y, z):
    return (x & y) ^ (x & z) ^ (y & z)

def big_sigma0(x):
    return rotr(x, 2) ^ rotr(x, 13) ^ rotr(x, 22)

def big_sigma1(x):
    return rotr(x, 6) ^ rotr(x, 11) ^ rotr(x, 25)

def small_sigma0(x):
    return rotr(x, 7) ^ rotr(x, 18) ^ (x >> 3)

def small_sigma1(x):
    return rotr(x, 17) ^ rotr(x, 19) ^ (x >> 10)

K = [
    0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,
    0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,
    0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,
    0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,
    0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,
    0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,
    0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,
    0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,
    0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,
    0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,
    0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,
    0xd192e819,0xd6990624,0xf40e3585,0x106aa070,
    0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,
    0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,
    0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,
    0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2
]

def sha256(message):
    msg = []
    for c in message:
        msg.append(ord(c))

    bit_len = len(msg) * 8
    msg.append(0x80)

    while (len(msg) * 8) % 512 != 448:
        msg.append(0)

    length_bytes = []
    i = 7
    while i >= 0:
        length_bytes.append((bit_len >> (i * 8)) & 0xff)
        i -= 1

    msg += length_bytes

    h0 = 0x6a09e667
    h1 = 0xbb67ae85
    h2 = 0x3c6ef372
    h3 = 0xa54ff53a
    h4 = 0x510e527f
    h5 = 0x9b05688c
    h6 = 0x1f83d9ab
    h7 = 0x5be0cd19

    i = 0
    while i < len(msg):
        chunk = msg[i:i+64]
        w = [0] * 64

        j = 0
        while j < 16:
            w[j] = (chunk[j*4] << 24) | (chunk[j*4+1] << 16) | (chunk[j*4+2] << 8) | chunk[j*4+3]
            j += 1

        j = 16
        while j < 64:
            w[j] = (small_sigma1(w[j-2]) + w[j-7] + small_sigma0(w[j-15]) + w[j-16]) & 0xffffffff
            j += 1

        a = h0
        b = h1
        c = h2
        d = h3
        e = h4
        f = h5
        g = h6
        h = h7

        j = 0
        while j < 64:
            t1 = (h + big_sigma1(e) + ch(e, f, g) + K[j] + w[j]) & 0xffffffff
            t2 = (big_sigma0(a) + maj(a, b, c)) & 0xffffffff

            h = g
            g = f
            f = e
            e = (d + t1) & 0xffffffff
            d = c
            c = b
            b = a
            a = (t1 + t2) & 0xffffffff

            j += 1

        h0 = (h0 + a) & 0xffffffff
        h1 = (h1 + b) & 0xffffffff
        h2 = (h2 + c) & 0xffffffff
        h3 = (h3 + d) & 0xffffffff
        h4 = (h4 + e) & 0xffffffff
        h5 = (h5 + f) & 0xffffffff
        h6 = (h6 + g) & 0xffffffff
        h7 = (h7 + h) & 0xffffffff

        i += 64

    result = ""
    for x in [h0,h1,h2,h3,h4,h5,h6,h7]:
        result += hex(x)[2:].zfill(8)
    return result

text = input("Enter message: ")
print("SHA-256 =", sha256(text))
