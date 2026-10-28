# 링크 : https://jungol.co.kr/problem/2261
import sys
from collections import deque

input = sys.stdin.readline

def bfs(start:int, target:int, n:int, graph:list) -> list:
    parent:list = [0] * (n + 1)
    visited:list = [False] * (n + 1)

    queue = deque([start])
    visited[start] = True

    found:bool = False

    while queue:
        current_node:int = queue.popleft()

        if current_node == target:
            found = True
            break

        for next_node in graph[current_node]:
            if not visited[next_node]:
                visited[next_node] = True
                parent[next_node] = current_node
                queue.append(next_node)

    # 경로가 존재하지 않는 경우
    if not found:
        return [-1]

    # parent 배열을 타고 거꾸로 올라가며 경로 역추적
    path:list = []
    current_node = target
    while current_node != 0:
        path.append(current_node)
        current_node = parent[current_node]

    # 시작점(A)부터 도착점(B) 순서가 되도록 뒤집음
    path.reverse()
    return path

N, K = map(int, input().split())
codes:list = [0] + [int(input().rstrip(), 2) for _ in range(N)]
A, B = map(int, input().split())

graph:list = [[] for _ in range(N + 1)]
for i in range(1, N + 1, 1):
    value_i:int = codes[i]
    for j in range(i + 1, N + 1, 1):
        diff:int = value_i ^ codes[j]
        # 켜진 비트가 1개인지 판별 (해밍 거리가 1인지 확인)
        if diff and not (diff & (diff - 1)):
            graph[i].append(j)
            graph[j].append(i)

result:list = bfs(A, B, N, graph)
print(*result)