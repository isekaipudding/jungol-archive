# 링크 : https://jungol.co.kr/problem/5947
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())

if not (1 <= N <= 50) or not N & 1 :
    print("INPUT ERROR!")
    sys.exit(0)

L:list = []

for i in range(1, (N + 3) // 2, 1) :
    L.append(i)
    print(*L)

while L :
    if len(L) >= (N + 1) // 2 :
        L.pop()
        continue
    print(*L)
    L.pop()