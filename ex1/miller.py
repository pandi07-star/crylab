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

if n == 2 or n == 3:
    print("Probably Prime")
elif n < 2 or n % 2 == 0:
    print("Composite")
else:
    d = n - 1
    r = 0
    while d % 2 == 0:
        d = d // 2
        r += 1

    prime = True
    a = 2
    count = 0

    while count < k and a < n:
        x = mod_exp(a, d, n)

        if x != 1 and x != n - 1:
            skip = False
            i = 0
            while i < r - 1:
                x = (x * x) % n
                if x == n - 1:
                    skip = True
                    break
                i += 1
            if not skip:
                prime = False
                break

        count += 1
        a += 1

    if prime:
        print("Probably Prime")
    else:
        print("Composite")
