# 링크 : https://jungol.co.kr/problem/5945
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())

if not (1 <= N <= 50) or not N & 1 :
    print("INPUT ERROR!")
    sys.exit(0)

L:list = [[] for _ in range(N)]

number:int = 0

for i in range(N) :
    for j in range(i + 1) :
        number += 1
        L[i].append(number)

for i in range(N) :
    if i & 1 :
        L[i].reverse()

for i in range(N) :
    print(*L[i])