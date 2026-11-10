# 링크 : https://jungol.co.kr/problem/1453
import sys

input = sys.stdin.readline

M:int = int(input().rstrip())
N:int = M

factors:list = []

while N % 2 == 0:
    factors.append(2)
    N //= 2

divisor:int = 3
while divisor * divisor <= N:
    if N % divisor == 0:
        while N % divisor == 0:
            factors.append(divisor)
            N //= divisor
    divisor += 2

if N > 1:
    factors.append(N)


A:int = (M + 2) // 3

TWO = 0

for prime in factors:
    if prime != 2:
        break
    TWO += 1

B:int = len(factors) - (TWO // 2)

print(A, B)