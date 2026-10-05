# 링크 : https://jungol.co.kr/problem/8560
import sys

input = sys.stdin.readline

N:int = 10
L:list = [None for _ in range(N)]

for i in range(N):
    name, age = map(str, input().split())
    L[i] = (name, int(age))

L.sort(key=lambda x: (-x[1], x[0]))

for i in range(N):
    print(*L[i])