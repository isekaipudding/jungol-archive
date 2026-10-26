# 링크 : https://jungol.co.kr/problem/7095
import sys
import math

input = sys.stdin.readline
gcd = math.gcd

N:int = int(input().rstrip())
L:list = list(map(int, input().split()))

b, c = 1, L[N - 1]

# 1/{a + b/c} = c / (ac + b)
for i in range(N - 2, -1, -1):
    a = L[i]
    b, c = c, a * c + b
    g = gcd(b, c)
    b //= g
    c //= g

# 1 - b/c = (c - b) / c
b = c - b

print(b, c)