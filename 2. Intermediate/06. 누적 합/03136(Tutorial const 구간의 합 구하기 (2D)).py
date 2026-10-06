# 링크 : https://jungol.co.kr/problem/3136
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())

graph:list = []

for _ in range(N):
    graph.append(list(map(int, input().split())))

prefix:list = [[0 for _ in range(N + 1)] for _ in range(N + 1)]

for r in range(1, N + 1, 1):
    for c in range(1, N + 1, 1):
        prefix[r][c] = prefix[r][c-1] + graph[r-1][c-1]

for c in range(1, N + 1, 1):
    for r in range(1, N + 1, 1):
        prefix[r][c] = prefix[r-1][c] + prefix[r][c]

Q:int = int(input().rstrip())

for _ in range(Q):
    sr, sc, er, ec = map(int, input().split())
    result:int = prefix[er][ec] - prefix[sr - 1][ec] - prefix[er][sc - 1] + prefix[sr - 1][sc - 1]
    print(result)