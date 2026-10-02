# 링크 : https://jungol.co.kr/problem/2074
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())

graph:list = [[0 for _ in range(N)] for _ in range(N)]

index:int = 1

r, c = 0, (N - 1) // 2
while index <= N * N :
    graph[r][c] = index
    if index % N :
        r, c = (r - 1) % N, (c - 1) % N
    else :
        r = (r + 1) % N
    index += 1

for i in range(N) :
    print(*graph[i])