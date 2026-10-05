# 링크 : https://jungol.co.kr/problem/2194
import sys

input = sys.stdin.readline

N, S = map(int, input().split())

result:int = 0

a:int = float('inf')

for _ in range(N):
    C, Y = map(int, input().split())
    result += min(a + S, C) * Y
    a = min(a + S, C)

print(result)