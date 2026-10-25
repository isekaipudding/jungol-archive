# 링크 : https://jungol.co.kr/problem/1840
import sys

sys.setrecursionlimit(1 << 20)
input = sys.stdin.readline

dr = (-1, 1, 0, 0)
dc = (0, 0, -1, 1)

def dfs(r:int, c:int, visited:list, melting_list:list) -> None:
    visited[r][c] = True

    for i in range(4):
        nr = r + dr[i]
        nc = c + dc[i]

        if 0 <= nr < R and 0 <= nc < C and not visited[nr][nc]:
            visited[nr][nc] = True
            if graph[nr][nc] == 0:
                # 바깥 공기면 계속 타고 들어감
                dfs(nr, nc, visited, melting_list)
            elif graph[nr][nc] == 1:
                # 공기와 닿은 치즈 표면이면 녹을 대상에 등록(더 깊이 들어가진 않음)
                melting_list.append((nr, nc))

R, C = map(int, input().split())
graph:list = [list(map(int, input().split())) for _ in range(R)]

# 전체 치즈 칸 수 계산
total_cheese:int = sum(row.count(1) for row in graph)
time:int = 0
last_cheese_count:int = 0

# 치즈가 전부 녹을 때까지 1시간 단위 시뮬레이션 반복
while total_cheese > 0:
    # 녹기 직전의 치즈 개수 보존
    last_cheese_count = total_cheese

    visited = [[False] * C for _ in range(R)]
    melting_list = []

    # (0, 0)은 문제 조건상 항상 바깥 공기
    dfs(0, 0, visited, melting_list)

    # 공기와 닿았던 치즈를 공기(0)로 녹임
    for r, c in melting_list:
        graph[r][c] = 0

    # 남은 치즈 개수 차감 및 시간 증가
    total_cheese -= len(melting_list)
    time += 1

print(time)
print(last_cheese_count)