def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

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
q = int(input("Enter prime q: "))
m = int(input("Enter message: "))

n = p * q
phi = (p - 1) * (q - 1)

e = 2
while gcd(e, phi) != 1:
    e += 1

d = 1
while (d * e) % phi != 1:
    d += 1

c = mod_exp(m, e, n)
plain = mod_exp(c, d, n)

print("n =", n)
print("phi =", phi)
print("e =", e)
print("d =", d)
print("Ciphertext =", c)
print("Decrypted message =", plain)
