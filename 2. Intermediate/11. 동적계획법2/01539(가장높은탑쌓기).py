# 링크 : https://jungol.co.kr/problem/1539
import sys

input = sys.stdin.readline

N = int(input().rstrip())

# 예외 처리
if N == 0:
    print(0)
    sys.exit(0)

# bricks : (벽돌 번호, 밑면 넓이, 높이, 무게)
bricks:list = []
for brick_id in range(1, N + 1, 1):
    area, height, weight = map(int, input().split())
    bricks.append((brick_id, area, height, weight))

# 밑면 넓이 기준 내림차순 정렬(아래 깔릴 벽돌이 앞에 오도록)
bricks.sort(key=lambda x: x[1], reverse=True)

# i번째 벽돌을 맨 위에 올렸을 때 탑의 최대 높이
dp:list = [0] * N
# i번째 벽돌 바로 아래에 위치한 벽돌의 인덱스
parent:list = [-1] * N

# 점화식
for i in range(N):
    dp[i] = bricks[i][2] # 자기 자신의 높이로 초기화
    for j in range(i):
        # j번 벽돌의 무게가 i번보다 무거우면 j 위에 i를 쌓을 수 있음
        if bricks[j][3] > bricks[i][3]:
            if dp[j] + bricks[i][2] > dp[i]:
                dp[i] = dp[j] + bricks[i][2]
                parent[i] = j

# 최대 높이를 만드는 꼭대기 벽돌(top_index) 탐색
max_height = -1
top_index = -1
for i in range(N):
    if dp[i] > max_height:
        max_height = dp[i]
        top_index = i

# 꼭대기부터 바닥까지 역추적(Top -> Bottom)
result = []
current = top_index
while current != -1:
    result.append(bricks[current][0]) # 벽돌의 원래 번호 저장
    current = parent[current]

print(len(result))
for brick_id in result:
    print(brick_id)