# 링크 : https://jungol.co.kr/problem/1457
import sys

sys.setrecursionlimit(1 << 20)
input = sys.stdin.readline

# 아까 전에 나온 단자번호붙이기(정올 1695번) 문제에서 이전에는 색칠된 영역을 구할려면
# 이 문제는 색칠되지 않는 영역을 구하는 문제이네요.
# 연결 요소 문제라서 푸는게 큰 어려움이 없었어요.

dr = (-1, 1, 0, 0)
dc = (0, 0, -1, 1)

def dfs(r:int, c:int) -> int:
    # 다시 방문하지 않도록 1(벽)로 덮어씀
    graph[r][c] = 1
    area:int = 1

    for i in range(4):
        nr:int = r + dr[i]
        nc:int = c + dc[i]

        # 모눈종이 내부(0 <= nr < M, 0 <= nc < N)이고 빈칸(0)인 경우
        if 0 <= nr < M and 0 <= nc < N and graph[nr][nc] == 0:
            area += dfs(nr, nc)

    return area

M, N, K = map(int, input().split())

# 0은 빈 영역, 1은 직사각형 내부(벽) 또는 이미 방문한 곳
graph:list = [[0] * N for _ in range(M)]

# K개의 직사각형 영역을 1로 마킹
for _ in range(K):
    x1, y1, x2, y2 = map(int, input().split())
    # r은 y좌표 범위 [y1, y2), c는 x좌표 범위 [x1, x2)
    for r in range(y1, y2):
        for c in range(x1, x2):
            graph[r][c] = 1

areas:list = []

# 전체 모눈종이를 순회하며 분리된 빈 영역 탐색
for r in range(M):
    for c in range(N):
        if graph[r][c] == 0:
            areas.append(dfs(r, c))

areas.sort()

print(len(areas))
print(*areas)