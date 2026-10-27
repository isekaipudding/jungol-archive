# 링크 : https://jungol.co.kr/problem/2462
import sys

sys.setrecursionlimit(1 << 20)
input = sys.stdin.readline

def dfs(current:int, graph:list, visited:list) -> int:
    count:int = 0
    for next_node in graph[current]:
        if not visited[next_node]:
            visited[next_node] = True
            count += 1 + dfs(next_node, graph, visited)
    return count

N, M = map(int, input().split())

# 정방향 : a -> b (a보다 b가 큼)
graph:list = [[] for _ in range(N + 1)]
# 역방향 : b -> a (b보다 a가 작음)
reverse_graph:list = [[] for _ in range(N + 1)]

for _ in range(M):
    a, b = map(int, input().split())
    graph[a].append(b)
    reverse_graph[b].append(a)

result:int = 0

for i in range(1, N + 1, 1):
    # i보다 확실히 큰 학생 수(정방향 DFS)
    visited_forward:list = [False] * (N + 1)
    visited_forward[i] = True
    taller_count:int = dfs(i, graph, visited_forward)

    # i보다 확실히 작은 학생 수(역방향 DFS)
    visited_backward:list = [False] * (N + 1)
    visited_backward[i] = True
    shorter_count:int = dfs(i, reverse_graph, visited_backward)

    # 나보다 큰 사람 + 나보다 작은 사람 == N - 1이면 등수 확정
    if taller_count + shorter_count == N - 1:
        result += 1

print(result)