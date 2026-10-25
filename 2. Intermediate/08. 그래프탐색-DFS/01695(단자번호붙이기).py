# 링크 : https://jungol.co.kr/problem/1695
import sys

sys.setrecursionlimit(1 << 20)
input = sys.stdin.readline

# 이것도 백준에 나온 문제입니다.

dr = (-1, 1, 0, 0)
dc = (0, 0, -1, 1)

def dfs(r:int, c:int) -> int:
    # 다시 방문하지 않도록 0으로 덮어씌움
    graph[r][c] = 0
    count:int = 1

    for i in range(4):
        nr = r + dr[i]
        nc = c + dc[i]

        # 지도 범위 내이고, 아직 방문하지 않은 집(1)인 경우 재귀 탐색
        if 0 <= nr < N and 0 <= nc < N and graph[nr][nc] == 1:
            count += dfs(nr, nc)

    return count

N:int = int(input().rstrip())
graph: list = [list(map(int, input().rstrip())) for _ in range(N)]

components: list = []

# 전체 그래프를 순회하며 새로운 단지의 시작점 탐색
for r in range(N):
    for c in range(N):
        if graph[r][c] == 1:
            # 연결 요소의 크기를 구해 리스트에 추가
            components.append(dfs(r, c))

# 단지 내 집의 수를 오름차순으로 정렬
components.sort()

# 첫째 줄에 총 단지 수, 다음 줄부터 각 단지의 크기 출력
print(len(components))
for size in components:
    print(size)