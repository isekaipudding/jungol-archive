# 링크 : https://jungol.co.kr/problem/1707
import sys
from collections import deque

input = sys.stdin.readline

directions:deque = deque([
    (0, 1),
    (1, 0),
    (0, -1),
    (-1, 0)
])

def check_graph_range(r:int, c:int) -> bool :
    if 0 <= r < N and 0 <= c < N :
        return True
    return False

N:int = int(input().rstrip())

graph:list = [[0 for _ in range(N)] for _ in range(N)]

index:int = 1

r, c = 0, 0
while index <= N * N :
    graph[r][c] = index
    dr, dc = directions[0]
    nr, nc = r + dr, c + dc
    if check_graph_range(nr, nc) and graph[nr][nc] == 0 :
        r, c = nr, nc
    else :
        directions.rotate(-1)
        dr, dc = directions[0]
        r, c = r + dr, c + dc
    index += 1

for i in range(N) :
    print(*graph[i])