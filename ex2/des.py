P10 = [3,5,2,7,4,10,1,9,8,6]
P8 = [6,3,7,4,8,5,10,9]
IP = [2,6,3,1,4,8,5,7]
IP_INV = [4,1,3,5,7,2,8,6]
EP = [4,1,2,3,2,3,4,1]
P4 = [2,4,3,1]

S0 = [
    [1,0,3,2],
    [3,2,1,0],
    [0,2,1,3],
    [3,1,3,2]
]

S1 = [
    [0,1,2,3],
    [2,0,1,3],
    [3,0,1,0],
    [2,1,0,3]
]

def permute(bits, table):
    r = ""
    for i in table:
        r += bits[i - 1]
    return r

def left_shift(bits, n):
    return bits[n:] + bits[:n]

def xor(a, b):
    r = ""
    for i in range(len(a)):
        if a[i] == b[i]:
            r += "0"
        else:
            r += "1"
    return r

def sbox(bits, box):
    row = int(bits[0] + bits[3], 2)
    col = int(bits[1] + bits[2], 2)
    return bin(box[row][col])[2:].zfill(2)

def generate_keys(key):
    p10 = permute(key, P10)
    left = p10[:5]
    right = p10[5:]

    left = left_shift(left, 1)
    right = left_shift(right, 1)
    k1 = permute(left + right, P8)

    left = left_shift(left, 2)
    right = left_shift(right, 2)
    k2 = permute(left + right, P8)

    return k1, k2

def fk(bits, key):
    left = bits[:4]
    right = bits[4:]
    ep = permute(right, EP)
    x = xor(ep, key)
    s0 = sbox(x[:4], S0)
    s1 = sbox(x[4:], S1)
    p4 = permute(s0 + s1, P4)
    left = xor(left, p4)
    return left + right

def switch(bits):
    return bits[4:] + bits[:4]

def encrypt(pt, key):
    k1, k2 = generate_keys(key)
    ip = permute(pt, IP)
    r1 = fk(ip, k1)
    r2 = fk(switch(r1), k2)
    return permute(r2, IP_INV)

def decrypt(ct, key):
    k1, k2 = generate_keys(key)
    ip = permute(ct, IP)
    r1 = fk(ip, k2)
    r2 = fk(switch(r1), k1)
    return permute(r2, IP_INV)

key = input("Enter 10-bit key: ")
text = input("Enter 8-bit text: ")
mode = input("Enter mode (encrypt/decrypt): ")

if mode == "encrypt":
    print("Ciphertext:", encrypt(text, key))
else:
    print("Plaintext:", decrypt(text, key))
