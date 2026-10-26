# 링크 : https://jungol.co.kr/problem/3285
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())

result:list = []

while N % 2 == 0:
    result.append(2)
    N //= 2

divisor:int = 3
while divisor * divisor <= N:
    if N % divisor == 0:
        while N % divisor == 0:
            result.append(divisor)
            N //= divisor
    divisor += 2

if N > 1:
    result.append(N)

print(*result)