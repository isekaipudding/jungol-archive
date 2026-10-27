# 링크 : https://jungol.co.kr/problem/1681
import sys

sys.setrecursionlimit(1 << 20)
input = sys.stdin.readline

def dfs(u:int, visited:int, current_cost:int) -> None:
    global min_cost

    # 현재까지의 이동 비용이 이미 완성된 최소 비용 이상이면 더 이상 탐색하지 않음
    if current_cost >= min_cost:
        return

    # 모든 장소를 전부 방문한 경우
    if visited == ALL_VISITED:
        # 마지막 정점 u에서 출발지(0번, 회사)로 돌아가는 유효 간선이 존재하는지 검사
        if graph[u][0] != 0:
            cost_to_home = current_cost + graph[u][0]
            if cost_to_home < min_cost:
                min_cost = cost_to_home
        return

    # 현재 정점 u의 연결 행을 가져와 다음 방문할 장소 v 탐색
    row = graph[u]
    for v in range(N):
        # 1. 아직 방문하지 않은 장소이고
        # 2. 이동 경로가 존재하는 경우(graph[u][v] != 0)
        if not (visited & (1 << v)) and row[v] != 0:
            dfs(v, visited | (1 << v), current_cost + row[v])

N:int = int(input().rstrip())
graph:list = [list(map(int, input().split())) for _ in range(N)]

# 배달할 장소가 회사 1곳뿐인 경우 예외 처리
if N == 1:
    print(0)
    sys.exit(0)

ALL_VISITED:int = (1 << N) - 1
min_cost = float('inf')

# 0번(1번 장소, 회사)에서 시작, 0번 비트 켜짐(1 << 0 = 1)
dfs(0, 1, 0)

print(min_cost if min_cost != float('inf') else 0)