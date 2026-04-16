def myPow(x, n):
    if n == 0:
        return 1.0
    
    if n < 0:
        x = 1 / x
        n = -n
    
    result = 1.0
    
    while n > 0:
        if n % 2 == 1:
            result *= x
        
        x *= x
        n //= 2
    
    return result


# Examples
print(myPow(2.0, 10))
print(myPow(2.1, 3))
print(myPow(2.0, -2))
