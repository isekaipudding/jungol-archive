# 링크 : https://jungol.co.kr/problem/1006
import sys
from collections import deque

input = sys.stdin.readline

# 시계방향 순서 정의 : 동(0), 남(1), 서(2), 북(3)
dr = (0, 1, 0, -1)
dc = (1, 0, -1, 0)

# 입력 방향(1:동, 2:서, 3:남, 4:북) -> 시계방향 인덱스 변환 매핑
DIR_MAP = {
    1: 0,
    2: 2,
    3: 1,
    4: 3
}

def bfs(sr:int, sc:int, sd:int, tr:int, tc:int, td:int, m:int, n:int, graph:list) -> int:
    # 출발점과 도착점의 위치 및 방향이 완전히 같은 경우
    if sr == tr and sc == tc and sd == td:
        return 0

    # distance[r][c][d] : (r, c) 위치에서 d 방향을 바라볼 때의 최소 명령 횟수(여기서 -1로 초기화)
    distance:list = [[[-1] * 4 for _ in range(n)] for _ in range(m)]

    queue = deque([(sr, sc, sd)])
    distance[sr][sc][sd] = 0

    while queue:
        r, c, d = queue.popleft()

        # 목표 위치와 방향에 도달한 경우
        if r == tr and c == tc and d == td:
            return distance[r][c][d]

        # 명령 1 : Go k(여기서 1, 2, 3칸 직진)
        for k in range(1, 4):
            nr = r + dr[d] * k
            nc = c + dc[d] * k

            # 격자 범위를 벗어나면 더 이상 전진 불가
            if not (0 <= nr < m and 0 <= nc < n):
                break

            # 중간에 벽(1)을 만나면 그 너머로 갈 수 없으므로 즉시 break
            if graph[nr][nc] == 1:
                break

            # 아직 방문하지 않은 상태라면 큐에 추가
            if distance[nr][nc][d] == -1:
                distance[nr][nc][d] = distance[r][c][d] + 1
                queue.append((nr, nc, d))

        # 명령 2 : Turn(왼쪽 90도 회전, 오른쪽 90도 회전)
        turn = ((d + 1) % 4, (d + 3) % 4)
        for nd in turn:
            if distance[r][c][nd] == -1:
                distance[r][c][nd] = distance[r][c][d] + 1
                queue.append((r, c, nd))

    return -1

M, N = map(int, input().split())
graph:list = [list(map(int, input().split())) for _ in range(M)]

sr, sc, s_dir = map(int, input().split())
tr, tc, t_dir = map(int, input().split())

# 1-based index -> 0-based index
start_r, start_c, start_d = sr - 1, sc - 1, DIR_MAP[s_dir]
target_r, target_c, target_d = tr - 1, tc - 1, DIR_MAP[t_dir]

result:int = bfs(start_r, start_c, start_d, target_r, target_c, target_d, M, N, graph)
print(result)