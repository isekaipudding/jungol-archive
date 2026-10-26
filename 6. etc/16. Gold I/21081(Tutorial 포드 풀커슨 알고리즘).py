# 링크 : https://jungol.co.kr/problem/21081
import sys
from collections import deque

input = sys.stdin.readline

def bfs():
    parent:list = [-1] * (N + 1)
    parent[source] = source

    queue = deque([source])

    while queue:
        current_node = queue.popleft()
        if current_node == sink:
            break
        
        for next_node in graph[current_node]:
            if capacity[current_node][next_node] - flow[current_node][next_node] > 0 and parent[next_node] == -1:
                parent[next_node] = current_node
                queue.append(next_node)

    return parent

N, M = map(int, input().split())

capacity:list = [[0] * (N + 1) for _ in range(N + 1)]
flow:list = [[0] * (N + 1) for _ in range(N + 1)]
graph:list = [[] for _ in range(N + 1)]

for _ in range(M):
    u, v, c = map(int, input().split())
    capacity[u][v] += c
    graph[u].append(v)
    graph[v].append(u)

source:int = 1
sink:int = N

total_flow:int = 0

while True:
    parent = bfs()

    if parent[sink] == -1:
        break

    bottleneck = float('inf')

    current = sink

    while current != source:
        previous = parent[current]
        residual = capacity[previous][current] - flow[previous][current]
        bottleneck = min(bottleneck, residual)
        current = previous
    
    current = sink
    while current != source:
        previous = parent[current]
        flow[previous][current] += bottleneck
        flow[current][previous] -= bottleneck
        current = previous

    total_flow += bottleneck

print(total_flow)