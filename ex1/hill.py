def mod_inv(a, m):
    a = a % m
    x = 1
    while x < m:
        if (a * x) % m == 1:
            return x
        x += 1
    return -1

text = input("Enter text: ").upper().replace(" ", "")
mode = input("Enter mode (encrypt/decrypt): ")

k00 = int(input("Enter K[0][0]: "))
k01 = int(input("Enter K[0][1]: "))
k10 = int(input("Enter K[1][0]: "))
k11 = int(input("Enter K[1][1]: "))

if len(text) % 2 != 0:
    text += "X"

K = [[k00, k01], [k10, k11]]

if mode == "decrypt":
    det = (K[0][0] * K[1][1] - K[0][1] * K[1][0]) % 26
    inv_det = mod_inv(det, 26)
    if inv_det == -1:
        print("Key matrix is not invertible")
    else:
        K = [
            [(K[1][1] * inv_det) % 26, ((-K[0][1]) * inv_det) % 26],
            [((-K[1][0]) * inv_det) % 26, (K[0][0] * inv_det) % 26]
        ]

        result = ""
        i = 0
        while i < len(text):
            p1 = ord(text[i]) - 65
            p2 = ord(text[i+1]) - 65
            c1 = (K[0][0] * p1 + K[0][1] * p2) % 26
            c2 = (K[1][0] * p1 + K[1][1] * p2) % 26
            result += chr(c1 + 65)
            result += chr(c2 + 65)
            i += 2
        print("Result =", result)
else:
    result = ""
    i = 0
    while i < len(text):
        p1 = ord(text[i]) - 65
        p2 = ord(text[i+1]) - 65
        c1 = (K[0][0] * p1 + K[0][1] * p2) % 26
        c2 = (K[1][0] * p1 + K[1][1] * p2) % 26
        result += chr(c1 + 65)
        result += chr(c2 + 65)
        i += 2
    print("Result =", result)
