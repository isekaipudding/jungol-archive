# 링크 : https://jungol.co.kr/problem/2578
import sys
from collections import deque

input = sys.stdin.readline

# 두 축 평행 선분이 교차하거나 겹치는지 판별
def intersects(b1:tuple, b2:tuple) -> bool:
    return (
        b1[0] <= b2[2] and b2[0] <= b1[2] and
        b1[1] <= b2[3] and b2[1] <= b1[3]
    )

# 좌표 (px, py)가 해당 버스 노선 위에 있는지 판별
def point_on_bus(px:int, py:int, bus:tuple) -> bool:
    return bus[0] <= px <= bus[2] and bus[1] <= py <= bus[3]

def bfs(sx:int, sy:int, dx:int, dy:int, k:int, buses:list) -> int:
    queue = deque()
    distance:list = [-1] * k
    unvisited:list = []

    # 출발지와 목적지를 지나는 버스 분류
    target_buses:set = set()

    for i in range(k):
        bus = buses[i]
        # 출발점을 지나는 버스는 BFS 시작 큐에 적재
        if point_on_bus(sx, sy, bus):
            distance[i] = 1
            queue.append(i)
        else:
            unvisited.append(i)

        # 목적지를 지나는 버스 기록
        if point_on_bus(dx, dy, bus):
            target_buses.add(i)

    # 예외 처리 -> 출발지와 목적지를 환승 없이 한 번에 가는 버스가 있는 경우
    for start_bus in queue:
        if start_bus in target_buses:
            return 1

    # 버스 단위 BFS 탐색
    while queue:
        current_index = queue.popleft()
        current_bus = buses[current_index]
        current_distance = distance[current_index]

        next_unvisited:list = []

        for next_index in unvisited:
            # 현재 버스에서 갈아탈 수 있는 버스인 경우
            if intersects(current_bus, buses[next_index]):
                distance[next_index] = current_distance + 1

                # 목적지에 닿는 버스로 갈아탄 순간 즉시 반환
                if next_index in target_buses:
                    return distance[next_index]

                queue.append(next_index)
            else:
                next_unvisited.append(next_index)

        # 방문하지 않은 남은 버스 목록 갱신
        unvisited = next_unvisited

    return -1

m, n = map(int, input().split())
k = int(input().split()[0])

buses:list = []
for _ in range(k):
    b, x1, y1, x2, y2 = map(int, input().split())
    # 좌표 정규화(x_min, y_min, x_max, y_max)
    buses.append((
        min(x1, x2), min(y1, y2),
        max(x1, x2), max(y1, y2)
    ))

sx, sy, dx, dy = map(int, input().split())

print(bfs(sx, sy, dx, dy, k, buses))