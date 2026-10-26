# 링크 : https://jungol.co.kr/problem/2267
import sys

input = sys.stdin.readline

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

N:int = int(input().rstrip())
L:list = [0] * N

for i in range(N):
    L[i] = int(input().rstrip())

L.sort()

GCD = L[-1] - L[0]

for i in range(1, N, 1):
    GCD = gcd(GCD, L[i] - L[i - 1])

result:int = (L[-1] - L[0]) // GCD - N + 1

print(result)