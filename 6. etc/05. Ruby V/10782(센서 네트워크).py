# 링크 : https://jungol.co.kr/problem/10782
import sys

sys.setrecursionlimit(1 << 20)
input = sys.stdin.readline

# 에디토리얼 1 : https://justicehui.github.io/icpc/2019/12/25/BOJ10058/
# 에디토리얼 2 : https://alreadysolved.tistory.com/43

def get_distance(x1:int, y1:int, x2:int, y2:int) -> int:
    dx:int = x1 - x2
    dy:int = y1 - y2
    return dx * dx + dy * dy

def ccw(x1:int, y1:int, x2:int, y2:int, x3:int, y3:int) -> int:
    return (x2 - x1) * (y3 - y1) - (x3 - x1) * (y2 - y1)

def bipartite_matching(node:int) -> bool:
    for target in graph[node]:
        if visited[target]:
            continue
        visited[target] = True
        if left_match[target] == -1 or bipartite_matching(left_match[target]):
            left_match[target] = node
            right_match[node] = target
            return True
    return False

def mark_alternating(node:int) -> None:
    visited_upper[node] = True
    for target in graph[node]:
        if not cover_lower[target]:
            cover_lower[target] = True
            next_node:int = left_match[target]
            if next_node != -1 and not visited_upper[next_node]:
                mark_alternating(next_node)

number_sensors, max_distance = map(int, input().split())
limit_sq:int = max_distance * max_distance

position_x:list = [0] * (number_sensors + 1)
position_y:list = [0] * (number_sensors + 1)

for index in range(1, number_sensors + 1):
    position_x[index], position_y[index] = map(int, input().split())

result:list = [1]

graph:list = [[] for _ in range(number_sensors + 1)]
left_match:list = [-1] * (number_sensors + 1)
right_match:list = [-1] * (number_sensors + 1)
visited:list = [False] * (number_sensors + 1)
visited_upper:list = [False] * (number_sensors + 1)
cover_lower:list = [False] * (number_sensors + 1)

for i in range(1, number_sensors + 1, 1):
    for j in range(i + 1, number_sensors + 1, 1):
        radius_sq:int = get_distance(position_x[i], position_y[i], position_x[j], position_y[j])
        if radius_sq > limit_sq:
            continue

        upper:list = []
        lower:list = []

        for k in range(1, number_sensors + 1, 1):
            if (
                get_distance(position_x[i], position_y[i], position_x[k], position_y[k]) <= radius_sq
                and get_distance(position_x[j], position_y[j], position_x[k], position_y[k]) <= radius_sq
            ):
                if ccw(position_x[i], position_y[i], position_x[j], position_y[j], position_x[k], position_y[k]) >= 0:
                    upper.append(k)
                else:
                    lower.append(k)

        # 렌즈 내부의 전체 센서 수가 현재 최적해 이하이면 탐색 생략
        if len(upper) + len(lower) <= len(result):
            continue

        for u in upper:
            graph[u].clear()
            right_match[u] = -1

        for v in lower:
            left_match[v] = -1

        for u in upper:
            for v in lower:
                if get_distance(position_x[u], position_y[u], position_x[v], position_y[v]) > radius_sq:
                    graph[u].append(v)

        matched_count:int = 0
        for u in upper:
            for v in lower:
                visited[v] = False
            if bipartite_matching(u):
                matched_count += 1

        # 최대 독립 집합의 크기가 현재 최적해 이하이면 역추적 생략
        if len(upper) + len(lower) - matched_count <= len(result):
            continue

        for u in upper:
            visited_upper[u] = False
        for v in lower:
            cover_lower[v] = False

        # 매칭되지 않은 upper 정점에서 시작하여 교대 경로 탐색 
        # 최소 정점 덮개 구하기
        for u in upper:
            if right_match[u] == -1:
                mark_alternating(u)

        candidate:list = []
        for u in upper:
            if visited_upper[u]:
                candidate.append(u)
        for v in lower:
            if not cover_lower[v]:
                candidate.append(v)

        if len(candidate) > len(result):
            result = candidate

result.sort()
print(len(result))
print(*result)