# 링크 : https://jungol.co.kr/problem/1927
import sys

input = sys.stdin.readline

A, K = map(int, input().split())

result:int = -1
rem:int = 0

# 비둘기집 원리에 의해 해가 존재하면 K번 이내에 반드시 등장합니다.
for m in range(1, K + 1, 1):
    rem = (rem * 10 + A) % K
    if rem == 0:
        result = m
        break

print(result)