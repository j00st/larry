def odd(n):
    if(n==0):
        return False
    return even(n-1)

def even(n):
    if(n==0):
        return True
    return odd(n-1)

print(even(1))
print(odd(1))
print(even(7))
print(odd(7))
print(even(8))
print(odd(8))
print(even(9))
print(odd(9))
print(even(0))
print(odd(0))