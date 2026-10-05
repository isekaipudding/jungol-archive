# 링크 : https://jungol.co.kr/problem/3521
import sys

input = sys.stdin.readline

a, b, c, d, e, N = map(int, input().split())
L:list = [a, b, c, d, e]
COUNT:list = [0, 0, 0, 0, 0]

result:int = 0

for i in range(4, -1, -1):
    weight:int = 1 << i
    COUNT[i] = min(L[i], N // weight)
    N -= weight * COUNT[i]

if N:
    print("impossible")
else:
    print(sum(COUNT))