# 링크 : https://jungol.co.kr/problem/3230
import sys

sys.setrecursionlimit(1 << 20)
input = sys.stdin.readline

def dfs(current:int, total_distance:int, max_edge:int) -> int:
    # 로봇 2번 방에 도달하면 결과 계산 후 반환
    if current == R2:
        return total_distance - max_edge

    for next_node, weight in graph[current]:
        if not visited[next_node]:
            visited[next_node] = True
            result = dfs(
                next_node,
                total_distance + weight,
                max(max_edge, weight)
            )
            # R2를 찾아서 결과를 얻었다면 즉시 상위 호출로 전달
            if result != -1:
                return result

    return -1

N, R1, R2 = map(int, input().split())

# 2. 트리 인접 리스트 구성(방 번호, 통로 길이)
graph:list = [[] for _ in range(N + 1)]
for _ in range(N - 1):
    u, v, w = map(int, input().split())
    graph[u].append((v, w))
    graph[v].append((u, w))

visited:list = [False] * (N + 1)

# 두 로봇이 처음부터 같은 방에 있는 예외 처리
if R1 == R2:
    print(0)
else:
    visited[R1] = True
    print(dfs(R1, 0, 0))