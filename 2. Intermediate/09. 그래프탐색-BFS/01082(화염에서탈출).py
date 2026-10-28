# 링크 : https://jungol.co.kr/problem/1082
import sys
from collections import deque

input = sys.stdin.readline

dr = (-1, 1, 0, 0)
dc = (0, 0, -1, 1)

# 불의 확산 시간 계산 BFS
def spread():
    while fire_queue:
        r, c = fire_queue.popleft()

        for i in range(4):
            nr = r + dr[i]
            nc = c + dc[i]

            # 빈칸('.') 또는 재우의 시작 위치('S')로만 불이 번짐(단, 바위와 집은 제외)
            if 0 <= nr < R and 0 <= nc < C:
                if graph[nr][nc] in ('.', 'S') and fire_time[nr][nc] == float('inf'):
                    fire_time[nr][nc] = fire_time[r][c] + 1
                    fire_queue.append((nr, nc))


# 재우의 이동 BFS
def escape(sr:int, sc:int) -> str:
    jaewoo_queue = deque([(sr, sc, 0)])
    visited: list = [[False] * C for _ in range(R)]
    visited[sr][sc] = True

    while jaewoo_queue:
        r, c, t = jaewoo_queue.popleft()

        for i in range(4):
            nr = r + dr[i]
            nc = c + dc[i]

            if 0 <= nr < R and 0 <= nc < C and not visited[nr][nc]:
                # 목적지(용사의 집)에 도달한 경우 즉시 반환
                if graph[nr][nc] == 'D':
                    return str(t + 1)

                # 빈칸이며, 재우가 불보다 엄격히 먼저 도착할 수 있는 경우
                if graph[nr][nc] == '.' and (t + 1) < fire_time[nr][nc]:
                    visited[nr][nc] = True
                    jaewoo_queue.append((nr, nc, t + 1))

    return "impossible"

R, C = map(int, input().split())
graph:list = [list(input().rstrip()) for _ in range(R)]

fire_queue = deque()
fire_time:list = [[float('inf')] * C for _ in range(R)]

start_r = start_c = -1
dest_r = dest_c = -1

# 시작 위치, 목적지, 불의 초기 위치 파악
for r in range(R):
    for c in range(C):
        if graph[r][c] == '*':
            fire_queue.append((r, c))
            fire_time[r][c] = 0
        elif graph[r][c] == 'S':
            start_r, start_c = r, c
        elif graph[r][c] == 'D':
            dest_r, dest_c = r, c

spread()
result:str = escape(start_r, start_c)

print(result)