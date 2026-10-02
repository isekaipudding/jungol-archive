# 링크 : https://jungol.co.kr/problem/1337
import sys
from collections import deque

input = sys.stdin.readline

directions:deque = deque([
    (1, 1),
    (0, -1),
    (-1, 0)
])

def check_graph_range(r:int, c:int) -> bool :
    if 0 <= r < N and 0 <= c < N :
        return True
    return False

N:int = int(input().rstrip())

graph:list = [[None for _ in range(N)] for _ in range(N)]

index:int = 0

r, c = 0, 0
while index < N * (N + 1) // 2 :
    graph[r][c] = (index % 10)
    dr, dc = directions[0]
    nr, nc = r + dr, c + dc
    if check_graph_range(nr, nc) and graph[nr][nc] == None :
        r, c = nr, nc
    else :
        directions.rotate(-1)
        dr, dc = directions[0]
        r, c = r + dr, c + dc
    index += 1

result:list = [[] for _ in range(N)]

for i in range(N) :
    for j in range(N) :
        if graph[i][j] != None :
            result[i].append(graph[i][j])
        else :
            break

for i in range(N) :
    print(*result[i])