# 링크 : https://jungol.co.kr/problem/8577
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())

L:list = []
for i in range(1, N+1, 1) :
    s, e = map(int, input().split())
    L.append((i, s, e, e - s))

L.sort(key=lambda x: (x[3], x[1]))

for i in range(N) :
    print(L[i][0])