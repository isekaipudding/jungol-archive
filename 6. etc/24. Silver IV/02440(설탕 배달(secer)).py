# 링크 : https://jungol.co.kr/problem/2440
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())

result:int = 0

while N > 0:
    if N % 5 == 0:
        result += N // 5
        N = 0
        break
    N -= 3
    result += 1

if N:
    print(-1)
else:
    print(result)