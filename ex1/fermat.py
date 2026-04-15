def mod_exp(base, exp, mod):
    result = 1
    base = base % mod
    while exp > 0:
        if exp % 2 == 1:
            result = (result * base) % mod
        exp = exp // 2
        base = (base * base) % mod
    return result

n = int(input("Enter number to test: "))
k = int(input("Enter number of rounds: "))

if n == 2:
    print("Probably Prime")
elif n < 2 or n % 2 == 0:
    print("Composite")
else:
    prime = True
    a = 2
    count = 0

    while count < k and a < n:
        if mod_exp(a, n - 1, n) != 1:
            prime = False
            break
        count += 1
        a += 1

    if prime:
        print("Probably Prime")
    else:
        print("Composite")
