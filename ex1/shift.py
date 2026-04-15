text = input("Enter text: ").upper()
k = int(input("Enter shift key: "))
mode = input("Enter mode (encrypt/decrypt): ")

result = ""
k = k % 26

for ch in text:
    if ch >= 'A' and ch <= 'Z':
        x = ord(ch) - 65
        if mode == "encrypt":
            y = (x + k) % 26
        else:
            y = (x - k + 26) % 26
        result += chr(y + 65)
    else:
        result += ch

print("Result =", result)
