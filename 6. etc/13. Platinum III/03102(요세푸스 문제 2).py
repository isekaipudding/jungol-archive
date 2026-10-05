# 링크 : https://jungol.co.kr/problem/3102
import sys

input = sys.stdin.readline

LIMIT = 3

N, K = map(int, input().split())

result:list = []

for M in range(1, N + 1, 1):
    result = [(T + K) % M for T in result]
    
    if M <= LIMIT:
        result.append((K - 1) % M)

result = [T + 1 for T in result]
result.reverse()
print(*result)