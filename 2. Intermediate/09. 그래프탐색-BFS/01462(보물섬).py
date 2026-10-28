# 링크 : https://jungol.co.kr/problem/1462
import sys
from collections import deque

input = sys.stdin.readline

dr = (-1, 1, 0, 0)
dc = (0, 0, -1, 1)

def check_graph_range(r:int, c:int):
    if 0 <= r < R and 0 <= c < C:
        return True
    return False

def bfs(start_r:int, start_c:int) -> int:
    distance:list = [[-1] * C for _ in range(R)]
    queue = deque([(start_r, start_c)])
    distance[start_r][start_c] = 0

    max_distance:int = 0

    while queue:
        r, c = queue.popleft()

        for i in range(4):
            nr = r + dr[i]
            nc = c + dc[i]

            # 범위 내이고, 방문하지 않은 육지(L)인 경우
            if check_graph_range(nr, nc):
                if graph[nr][nc] == 'L' and distance[nr][nc] == -1:
                    d = distance[r][c] + 1
                    distance[nr][nc] = d
                    if d > max_distance:
                        max_distance = d
                    queue.append((nr, nc))

    return max_distance

R, C = map(int, input().split())
graph:list = [list(input().rstrip()) for _ in range(R)]

max_treasure_distance:int = 0

# 모든 좌표를 순회
for r in range(R):
    for c in range(C):
        if graph[r][c] == 'L':
            max_treasure_distance = max(max_treasure_distance, bfs(r, c))

print(max_treasure_distance)