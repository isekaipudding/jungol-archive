# 링크 : https://jungol.co.kr/problem/5349
import sys

input = sys.stdin.readline

L:list = list(map(str, input().split()))

result:list = []
for i in range(1, len(L), 2) :
    result.append(L[i])

result.reverse()

print(*result)