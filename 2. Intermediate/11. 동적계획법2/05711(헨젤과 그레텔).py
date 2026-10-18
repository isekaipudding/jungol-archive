# 링크 : https://jungol.co.kr/problem/5711
import sys

input = sys.stdin.readline

# 이거 골드 5티어 맞나요...?ㄷㄷㄷㄷ

# 두 경유지 (x1, y1) -> (x2, y2) 사이의 장애물을 피하는 경로 수 계산 함수
def count_paths(x1, y1, x2, y2) -> int:
    # sub_dp[i][j] : (x1, y1)에서 (i, j)까지 도달하는 경우의 수
    sub_dp = [[0] * (y2 + 1) for _ in range(x2 + 1)]

    # 초기식
    sub_dp[x1][y1] = 1

    # 점화식
    for i in range(x1, x2 + 1):
        for j in range(y1, y2 + 1):
            if (i, j) in obstacles:
                sub_dp[i][j] = 0
                continue

            # 위쪽 칸 (i - 1, j)에서 내려오는 경우
            if i > x1:
                sub_dp[i][j] += sub_dp[i - 1][j]

            # 왼쪽 칸 (i, j - 1)에서 오른쪽으로 이동하는 경우
            if j > y1:
                sub_dp[i][j] += sub_dp[i][j - 1]

    return sub_dp[x2][y2]

N, M, A, B = map(int, input().split())

pebbles = [tuple(map(int, input().split())) for _ in range(A)]
obstacles = set(tuple(map(int, input().split())) for _ in range(B))

# 예외 처리 1 : 출발지나 도착지에 장애물이 있는 경우
if (1, 1) in obstacles or (N, M) in obstacles:
    print(0)
    sys.exit(0)

# 예외 처리 2 : 조약돌 위치에 장애물이 겹쳐 있는 경우
for p in pebbles:
    if p in obstacles:
        print(0)
        sys.exit(0)

# 조약돌을 X 오름차순, 같다면 Y 오름차순으로 정렬
pebbles.sort(key=lambda p: (p[0], p[1]))

# 예외 처리 3 : 이동 규칙(+X, +Y)상 조약돌을 모두 줍는 순서가 성립하지 않는 경우
# X가 증가하는데 Y가 이전 조약돌보다 작아지는 순간 수집 불가
for i in range(A - 1):
    if pebbles[i][1] > pebbles[i + 1][1]:
        print(0)
        sys.exit(0)

# 예외 처리 4 : 조약돌이 격자 범위를 벗어나는 경우
if pebbles[0][0] < 1 or pebbles[0][1] < 1 or pebbles[-1][0] > N or pebbles[-1][1] > M:
    print(0)
    sys.exit(0)

# 반드시 순서대로 거쳐야 하는 경유지(Waypoints) 구성
# (1, 1) -> P_1 -> P_2 -> ... -> P_A -> (N, M)
waypoints:list = []
if pebbles[0] != (1, 1):
    waypoints.append((1, 1))
waypoints.extend(pebbles)
if waypoints[-1] != (N, M):
    waypoints.append((N, M))

# 각 구간별 경로의 수를 곱의 법칙으로 누적
total_ways:int = 1
for k in range(len(waypoints) - 1):
    x1, y1 = waypoints[k]
    x2, y2 = waypoints[k + 1]
    
    ways = count_paths(x1, y1, x2, y2)
    # 예외 처리 5 : 두 경유지 사이의 경로가 장애물로 완전히 가로막혀 도달할 수 없는 경우
    if ways == 0:
        print(0)
        sys.exit(0)
    total_ways *= ways

# 최종 경우의 수 출력
print(total_ways)