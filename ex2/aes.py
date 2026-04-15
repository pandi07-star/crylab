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

inv_sbox = [
82,9,106,213,48,54,165,56,191,64,163,158,129,243,215,251,
124,227,57,130,155,47,255,135,52,142,67,68,196,222,233,203,
84,123,148,50,166,194,35,61,238,76,149,11,66,250,195,78,
8,46,161,102,40,217,36,178,118,91,162,73,109,139,209,37,
114,248,246,100,134,104,152,22,212,164,92,204,93,101,182,146,
108,112,72,80,253,237,185,218,94,21,70,87,167,141,157,132,
144,216,171,0,140,188,211,10,247,228,88,5,184,179,69,6,
208,44,30,143,202,63,15,2,193,175,189,3,1,19,138,107,
58,145,17,65,79,103,220,234,151,242,207,206,240,180,230,115,
150,172,116,34,231,173,53,133,226,249,55,232,28,117,223,110,
71,241,26,113,29,41,197,137,111,183,98,14,170,24,190,27,
252,86,62,75,198,210,121,32,154,219,192,254,120,205,90,244,
31,221,168,51,136,7,199,49,177,18,16,89,39,128,236,95,
96,81,127,169,25,181,74,13,45,229,122,159,147,201,156,239,
160,224,59,77,174,42,245,176,200,235,187,60,131,83,153,97,
23,43,4,126,186,119,214,38,225,105,20,99,85,33,12,125
]

rcon = [1,2,4,8,16,32,64,128,27,54]

def hex_to_bytes(h):
    arr = []
    i = 0
    while i < len(h):
        arr.append(int(h[i:i+2], 16))
        i += 2
    return arr

def bytes_to_hex(arr):
    s = ""
    for x in arr:
        s += hex(x)[2:].zfill(2)
    return s

def gmul(a, b):
    p = 0
    for i in range(8):
        if b & 1:
            p ^= a
        hi = a & 128
        a = (a << 1) & 255
        if hi:
            a ^= 27
        b >>= 1
    return p

def sub_word(word):
    return [sbox[word[0]], sbox[word[1]], sbox[word[2]], sbox[word[3]]]

def rot_word(word):
    return [word[1], word[2], word[3], word[0]]

def key_expansion(key):
    words = []
    i = 0
    while i < 16:
        words.append([key[i], key[i+1], key[i+2], key[i+3]])
        i += 4

    i = 4
    while i < 44:
        temp = words[i - 1][:]
        if i % 4 == 0:
            temp = sub_word(rot_word(temp))
            temp[0] ^= rcon[(i // 4) - 1]
        new_word = [
            words[i - 4][0] ^ temp[0],
            words[i - 4][1] ^ temp[1],
            words[i - 4][2] ^ temp[2],
            words[i - 4][3] ^ temp[3]
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

def inv_sub_bytes(state):
    i = 0
    while i < 16:
        state[i] = inv_sbox[state[i]]
        i += 1

def shift_rows(state):
    t = state[:]
    state[1], state[5], state[9], state[13] = t[5], t[9], t[13], t[1]
    state[2], state[6], state[10], state[14] = t[10], t[14], t[2], t[6]
    state[3], state[7], state[11], state[15] = t[15], t[3], t[7], t[11]

def inv_shift_rows(state):
    t = state[:]
    state[1], state[5], state[9], state[13] = t[13], t[1], t[5], t[9]
    state[2], state[6], state[10], state[14] = t[10], t[14], t[2], t[6]
    state[3], state[7], state[11], state[15] = t[7], t[11], t[15], t[3]

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

def inv_mix_columns(state):
    c = 0
    while c < 4:
        i = c * 4
        a0, a1, a2, a3 = state[i], state[i+1], state[i+2], state[i+3]
        state[i]   = gmul(a0,14) ^ gmul(a1,11) ^ gmul(a2,13) ^ gmul(a3,9)
        state[i+1] = gmul(a0,9) ^ gmul(a1,14) ^ gmul(a2,11) ^ gmul(a3,13)
        state[i+2] = gmul(a0,13) ^ gmul(a1,9) ^ gmul(a2,14) ^ gmul(a3,11)
        state[i+3] = gmul(a0,11) ^ gmul(a1,13) ^ gmul(a2,9) ^ gmul(a3,14)
        c += 1

def encrypt_block(plain_hex, key_hex):
    state = hex_to_bytes(plain_hex)
    key = hex_to_bytes(key_hex)
    rks = key_expansion(key)

    add_round_key(state, rks[0])

    r = 1
    while r < 10:
        sub_bytes(state)
        shift_rows(state)
        mix_columns(state)
        add_round_key(state, rks[r])
        r += 1

    sub_bytes(state)
    shift_rows(state)
    add_round_key(state, rks[10])

    return bytes_to_hex(state)

def decrypt_block(cipher_hex, key_hex):
    state = hex_to_bytes(cipher_hex)
    key = hex_to_bytes(key_hex)
    rks = key_expansion(key)

    add_round_key(state, rks[10])

    r = 9
    while r > 0:
        inv_shift_rows(state)
        inv_sub_bytes(state)
        add_round_key(state, rks[r])
        inv_mix_columns(state)
        r -= 1

    inv_shift_rows(state)
    inv_sub_bytes(state)
    add_round_key(state, rks[0])

    return bytes_to_hex(state)

text = input("Enter 32-hex text: ")
key = input("Enter 32-hex key: ")
mode = input("Enter mode (encrypt/decrypt): ")

if mode == "encrypt":
    print("Ciphertext:", encrypt_block(text, key))
else:
    print("Plaintext:", decrypt_block(text, key))
