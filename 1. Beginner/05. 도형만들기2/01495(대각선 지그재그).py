# 링크 : https://jungol.co.kr/problem/1495
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())

graph:list = [[0 for _ in range(N)] for _ in range(N)]

index:int = 1

# s = r + c
for s in range(2 * (N - 1) + 1) :
    if s & 1 :
        for r in range(min(N - 1, s), max(-1, s - N), -1) :
            c:int = s - r
            graph[r][c] = index
            index += 1
    else :
        for c in range(min(N - 1, s), max(-1, s - N), -1) :
            r:int = s - c
            graph[r][c] = index
            index += 1

for i in range(N) :
    print(*graph[i])