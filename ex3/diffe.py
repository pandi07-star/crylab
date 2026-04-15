def mod_exp(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp // 2
        base = (base * base) % mod
    return result

p = int(input("Enter prime p: "))
g = int(input("Enter generator g: "))
a = int(input("Enter Alice secret a: "))
b = int(input("Enter Bob secret b: "))

A = mod_exp(g, a, p)
B = mod_exp(g, b, p)

key1 = mod_exp(B, a, p)
key2 = mod_exp(A, b, p)

print("Alice public key =", A)
print("Bob public key =", B)
print("Alice shared key =", key1)
print("Bob shared key =", key2)
