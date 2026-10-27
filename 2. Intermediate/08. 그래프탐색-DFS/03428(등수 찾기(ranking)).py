# 링크 : https://jungol.co.kr/problem/3428
import sys

sys.setrecursionlimit(1 << 20)
input = sys.stdin.readline

def dfs(current:int, graph:list, visited:list) -> int:
    visited[current] = True
    count:int = 1

    for next_node in graph[current]:
        if not visited[next_node]:
            count += dfs(next_node, graph, visited)

    return count

N, M, X = map(int, input().split())

# 정방향 : A -> B (A가 B보다 잘함, X보다 못한 사람들을 찾을 때 사용)
graph_worse:list = [[] for _ in range(N + 1)]
# 역방향 : B -> A (B 입장에서 A가 더 잘함, X보다 잘한 사람들을 찾을 때 사용)
graph_better:list = [[] for _ in range(N + 1)]

for _ in range(M):
    a, b = map(int, input().split())
    graph_worse[a].append(b)
    graph_better[b].append(a)

# X보다 확실히 잘한 학생 수 탐색(역방향 그래프)
visited_better:list = [False] * (N + 1)
better_count:int = dfs(X, graph_better, visited_better) - 1 # 자기 자신(X) 제외

# X보다 확실히 못한 학생 수 탐색(정방향 그래프)
visited_worse:list = [False] * (N + 1)
worse_count:int = dfs(X, graph_worse, visited_worse) - 1 # 자기 자신(X) 제외

# 등수 범위 계산
best_rank:int = 1 + better_count
worst_rank:int = N - worse_count

print(best_rank, worst_rank)