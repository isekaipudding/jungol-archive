# 링크 : https://jungol.co.kr/problem/8214
import sys
from collections import deque

input = sys.stdin.readline

directions:list = [
    (-1, 0), (-1, 1),
    (0, 1), (1, 1),
    (1, 0), (1, -1),
    (0, -1), (-1, -1)
]

def check_graph_range(R, C, r, c):
    if 0 <= r < R and 0 <= c < C:
        return True
    return False

def bfs():
    result:int = -1
    queue = deque()
    r, c = Y - M_y, M_x - 1
    R, C = Y, X
    queue.append((r, c))
    graph[r][c] = "M" # 여기를 안 넣어서 96.7% 반례가 발생했어요.
    """
    96.7% 반례
    2 1 1 1
    ..
    graph[r][c] 안 넣으면 2가 나옵니다.(정답 : 1)
    """
    while queue:
        result += 1
        TEMP:deque = deque()
        while queue:
            TEMP.append(queue.popleft())
        while TEMP:
            r, c = TEMP.popleft()
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if check_graph_range(R, C, nr, nc):
                    if graph[nr][nc] == ".":
                        graph[nr][nc] = "M"
                        queue.append((nr, nc))
    return result

X, Y, M_x, M_y = map(int, input().split())

graph:list = []

for _ in range(Y):
    graph.append(list(input().rstrip()))

print(bfs())