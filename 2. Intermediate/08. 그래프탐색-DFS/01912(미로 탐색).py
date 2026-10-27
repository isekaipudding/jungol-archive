# 링크 : https://jungol.co.kr/problem/1912
import sys

sys.setrecursionlimit(1 << 20)
input = sys.stdin.readline

def dfs(current:int) -> None:
    visited[current] = True
    visit_order.append(current)

    for next_node in graph[current]:
        # 아직 들르지 않은 방이라면 가장 작은 번호부터 재귀 탐색
        if not visited[next_node]:
            dfs(next_node)

N, M = map(int, input().split())

graph:list = [[] for _ in range(N + 1)]
for _ in range(M):
    u, v = map(int, input().split())
    graph[u].append(v)
    graph[v].append(v if False else u) # 양방향 연결

# 번호가 작은 방부터 우선 방문하도록 각 인접 리스트 오름차순 정렬
for i in range(1, N + 1, 1):
    graph[i].sort()

visited:list = [False] * (N + 1)
visit_order:list = []

dfs(1)

print(*visit_order)