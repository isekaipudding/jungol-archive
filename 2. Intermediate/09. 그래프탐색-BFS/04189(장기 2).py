# 링크 : https://jungol.co.kr/problem/4189
import sys
from collections import deque

input = sys.stdin.readline

dr = (
    -2, -2,
    -1, -1,
    1, 1,
    2, 2
)
dc = (
    -1, 1,
    -2, 2,
    -2, 2,
    -1, 1
)

def bfs(start_r:int, start_c:int, target_r:int, target_c:int, n:int, m:int) -> int:
    # 시작점과 목표점이 같은 경우 이동 횟수는 0
    if start_r == target_r and start_c == target_c:
        return 0

    # 1-based index(-1로 초기화)
    distance:list = [[-1] * (m + 1) for _ in range(n + 1)]

    queue = deque([(start_r, start_c)])
    distance[start_r][start_c] = 0

    while queue:
        r, c = queue.popleft()

        for i in range(8):
            nr = r + dr[i]
            nc = c + dc[i]

            # 장기판 범위 내부이고 아직 방문하지 않은 위치 탐색
            if 1 <= nr <= n and 1 <= nc <= m and distance[nr][nc] == -1:
                distance[nr][nc] = distance[r][c] + 1

                # 목표 지점(졸)에 도달하는 즉시 최소 거리 반환
                if nr == target_r and nc == target_c:
                    return distance[nr][nc]

                queue.append((nr, nc))

    return -1

N, M = map(int, input().split())
R, C, S, K = map(int, input().split())

print(bfs(R, C, S, K, N, M))