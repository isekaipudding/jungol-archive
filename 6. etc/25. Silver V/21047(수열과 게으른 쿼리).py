# 링크 : https://jungol.co.kr/problem/21047
import sys

input = sys.stdin.readline

N, Q = map(int, input().split())
total:int = sum(list(map(int, input().split())))

for _ in range(Q):
    query:list = list(map(int, input().split()))
    cmd:int = query[0]

    if cmd == 1:
        l, r, c = query[1], query[2], query[3]
        total += (r - l + 1) * c
    if cmd == 2:
        print(total)