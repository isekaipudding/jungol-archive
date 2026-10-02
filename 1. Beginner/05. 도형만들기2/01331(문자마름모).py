# 링크 : https://jungol.co.kr/problem/1331
import sys
from collections import deque

input = sys.stdin.readline

directions:deque = deque([
    (1, -1),
    (1, 1),
    (-1, 1),
    (-1, -1),
    (0, -1)
])

def check_graph_range(r:int, c:int) -> bool :
    if 0 <= r < 2 * N - 1 and 0 <= c < 2 * N - 1 :
        return True
    return False

N:int = int(input().rstrip())

graph:list = [[" " for _ in range(2 * N - 1)] for _ in range(2 * N - 1)]

for r in range(0, N - 1, 1) :
    for c in range(N - 1 - r, N + r, 1) :
        graph[r][c] = None
for r in range(N - 1, 2 * N - 1, 1) :
    for c in range(-(N - 1) + r, 3 * N - 2 - r, 1) :
        graph[r][c] = None

index:int = 0

r, c = 0, N - 1
while index < N * N + (N - 1) * (N - 1) :
    graph[r][c] = chr(65 + (index % 26))
    dr, dc = directions[0]
    nr, nc = r + dr, c + dc
    if check_graph_range(nr, nc) and graph[nr][nc] == None :
        r, c = nr, nc
    else :
        directions.rotate(-1)
        if index == N * N + (N - 1) * (N - 1) - 2 :
            directions.rotate(-1)
        dr, dc = directions[0]
        r, c = r + dr, c + dc
    index += 1

for i in range(2 * N - 1) :
    print(*graph[i])