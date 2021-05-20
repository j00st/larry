def sommig(n):
    result = 0
    while(n>=1):
        result += n
        n-=1
    return result

print(sommig(3))
print(sommig(8))
print(sommig(17))
print(sommig(33))