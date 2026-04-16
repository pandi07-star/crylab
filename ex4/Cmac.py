sbox = [
99,124,119,123,242,107,111,197,48,1,103,43,254,215,171,118,
202,130,201,125,250,89,71,240,173,212,162,175,156,164,114,192,
183,253,147,38,54,63,247,204,52,165,229,241,113,216,49,21,
4,199,35,195,24,150,5,154,7,18,128,226,235,39,178,117,
9,131,44,26,27,110,90,160,82,59,214,179,41,227,47,132,
83,209,0,237,32,252,177,91,106,203,190,57,74,76,88,207,
208,239,170,251,67,77,51,133,69,249,2,127,80,60,159,168,
81,163,64,143,146,157,56,245,188,182,218,33,16,255,243,210,
205,12,19,236,95,151,68,23,196,167,126,61,100,93,25,115,
96,129,79,220,34,42,144,136,70,238,184,20,222,94,11,219,
224,50,58,10,73,6,36,92,194,211,172,98,145,149,228,121,
231,200,55,109,141,213,78,169,108,86,244,234,101,122,174,8,
186,120,37,46,28,166,180,198,232,221,116,31,75,189,139,138,
112,62,181,102,72,3,246,14,97,53,87,185,134,193,29,158,
225,248,152,17,105,217,142,148,155,30,135,233,206,85,40,223,
140,161,137,13,191,230,66,104,65,153,45,15,176,84,187,22
]

rcon = [1,2,4,8,16,32,64,128,27,54]

def gmul(a, b):
    p = 0
    i = 0
    while i < 8:
        if b & 1:
            p ^= a
        hi = a & 128
        a = (a << 1) & 255
        if hi:
            a ^= 27
        b >>= 1
        i += 1
    return p

def rot_word(word):
    return [word[1], word[2], word[3], word[0]]

def sub_word(word):
    return [sbox[word[0]], sbox[word[1]], sbox[word[2]], sbox[word[3]]]

def key_expansion(key):
    words = []
    i = 0
    while i < 16:
        words.append([key[i], key[i+1], key[i+2], key[i+3]])
        i += 4

    i = 4
    while i < 44:
        temp = words[i-1][:]
        if i % 4 == 0:
            temp = sub_word(rot_word(temp))
            temp[0] ^= rcon[(i // 4) - 1]
        new_word = [
            words[i-4][0] ^ temp[0],
            words[i-4][1] ^ temp[1],
            words[i-4][2] ^ temp[2],
            words[i-4][3] ^ temp[3]
        ]
        words.append(new_word)
        i += 1

    round_keys = []
    i = 0
    while i < 44:
        rk = []
        rk += words[i]
        rk += words[i+1]
        rk += words[i+2]
        rk += words[i+3]
        round_keys.append(rk)
        i += 4
    return round_keys

def add_round_key(state, rk):
    i = 0
    while i < 16:
        state[i] ^= rk[i]
        i += 1

def sub_bytes(state):
    i = 0
    while i < 16:
        state[i] = sbox[state[i]]
        i += 1

def shift_rows(state):
    t = state[:]
    state[1], state[5], state[9], state[13] = t[5], t[9], t[13], t[1]
    state[2], state[6], state[10], state[14] = t[10], t[14], t[2], t[6]
    state[3], state[7], state[11], state[15] = t[15], t[3], t[7], t[11]

def mix_columns(state):
    c = 0
    while c < 4:
        i = c * 4
        a0, a1, a2, a3 = state[i], state[i+1], state[i+2], state[i+3]
        state[i]   = gmul(a0,2) ^ gmul(a1,3) ^ a2 ^ a3
        state[i+1] = a0 ^ gmul(a1,2) ^ gmul(a2,3) ^ a3
        state[i+2] = a0 ^ a1 ^ gmul(a2,2) ^ gmul(a3,3)
        state[i+3] = gmul(a0,3) ^ a1 ^ a2 ^ gmul(a3,2)
        c += 1

def aes_encrypt_block(block, key):
    state = block[:]
    round_keys = key_expansion(key)

    add_round_key(state, round_keys[0])

    r = 1
    while r < 10:
        sub_bytes(state)
        shift_rows(state)
        mix_columns(state)
        add_round_key(state, round_keys[r])
        r += 1

    sub_bytes(state)
    shift_rows(state)
    add_round_key(state, round_keys[10])

    return state

def xor_block(a, b):
    r = []
    i = 0
    while i < 16:
        r.append(a[i] ^ b[i])
        i += 1
    return r

def left_shift_one(block):
    out = [0] * 16
    carry = 0
    i = 15
    while i >= 0:
        val = block[i]
        out[i] = ((val << 1) & 255) | carry
        carry = (val >> 7) & 1
        i -= 1
    return out

def generate_subkeys(key):
    zero = [0] * 16
    L = aes_encrypt_block(zero, key)

    K1 = left_shift_one(L)
    if (L[0] & 128) != 0:
        K1[15] ^= 0x87

    K2 = left_shift_one(K1)
    if (K1[0] & 128) != 0:
        K2[15] ^= 0x87

    return K1, K2

def string_to_bytes(text):
    arr = []
    for c in text:
        arr.append(ord(c))
    return arr

def pad_block(block):
    while len(block) < 16:
        if len(block) == 0:
            block.append(128)
        else:
            if 128 not in block:
                block.append(128)
            else:
                block.append(0)
    return block

def cmac(message, key_text):
    key = string_to_bytes(key_text)
    while len(key) < 16:
        key.append(0)
    if len(key) > 16:
        key = key[:16]

    K1, K2 = generate_subkeys(key)

    data = string_to_bytes(message)

    n = len(data) // 16
    if len(data) % 16 != 0:
        n += 1

    if n == 0:
        n = 1

    blocks = []
    i = 0
    while i < n:
        start = i * 16
        end = start + 16
        blocks.append(data[start:end])
        i += 1

    if len(data) != 0 and len(data) % 16 == 0:
        last = xor_block(blocks[-1], K1)
    else:
        last_block = blocks[-1][:]
        if len(last_block) < 16:
            if len(last_block) < 16:
                last_block.append(128)
            while len(last_block) < 16:
                last_block.append(0)
        last = xor_block(last_block, K2)

    X = [0] * 16
    i = 0
    while i < n - 1:
        Y = xor_block(X, blocks[i])
        X = aes_encrypt_block(Y, key)
        i += 1

    Y = xor_block(X, last)
    T = aes_encrypt_block(Y, key)

    result = ""
    for b in T:
        result += hex(b)[2:].zfill(2)
    return result

message = input("Enter message: ")
key = input("Enter key (max 16 chars): ")
print("CMAC =", cmac(message, key))
