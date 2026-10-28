# 링크 : https://jungol.co.kr/problem/1078
import sys
from collections import deque

input = sys.stdin.readline

dr = (-1, 1, 0, 0)
dc = (0, 0, -1, 1)

def bfs(start_r:int, start_c:int, r_len:int, c_len:int, graph:list) -> tuple:
    # 각 저글링이 죽는 시간(-1은 미감염)
    death_time:list = [[-1] * c_len for _ in range(r_len)]

    queue = deque([(start_r, start_c)])
    # 시작 저글링은 감염 직후 3초 뒤에 사망
    death_time[start_r][start_c] = 3

    max_time:int = 3

    while queue:
        r, c = queue.popleft()

        for i in range(4):
            nr = r + dr[i]
            nc = c + dc[i]

            # 맵 범위 내이고, 저글링(1)이 있으며 아직 감염되지 않은 경우
            if 0 <= nr < r_len and 0 <= nc < c_len:
                if graph[nr][nc] == 1 and death_time[nr][nc] == -1:
                    # 이전 저글링 감염 1초 후 감염되므로 사망 시간도 +1
                    current_time: int = death_time[r][c] + 1
                    death_time[nr][nc] = current_time
                    if current_time > max_time:
                        max_time = current_time

                    queue.append((nr, nc))

    # 남아있는(감염되지 않아 죽지 않은) 저글링 수 집계
    survivors:int = 0
    for r in range(r_len):
        for c in range(c_len):
            if graph[r][c] == 1 and death_time[r][c] == -1:
                survivors += 1

    return max_time, survivors

C, R = map(int, input().split())
graph:list = [list(map(int, input().rstrip())) for _ in range(R)]

# 1-based -> 0-based 변환
target_c, target_r = map(int, input().split())
start_r, start_c = target_r - 1, target_c - 1

total_time, alive_zerglings = bfs(start_r, start_c, R, C, graph)

print(total_time)
print(alive_zerglings)