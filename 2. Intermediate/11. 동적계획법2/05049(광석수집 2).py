# 링크 : https://jungol.co.kr/problem/5049
import sys

input = sys.stdin.readline

N, M = map(int, input().split())
graph:list = [list(map(int, input().split())) for _ in range(N)]

# 예외 처리 : 출발지나 도착지가 바위(1)로 막혀 있는 경우 즉시 종료
if graph[0][0] == 1 or graph[N - 1][M - 1] == 1:
    print(0)
    sys.exit(0)

# (i, j)에 도달했을 때 얻는 최대 황금 개수(단, -1는 방문 불가)
dp = [[-1] * M for _ in range(N)]

# 초기식
dp[0][0] = 1 if graph[0][0] == 2 else 0

# 점화식
for i in range(N):
    for j in range(M):
        # 시작점은 이미 초기화했거나, 바위 칸이면 건너뜀
        if (i == 0 and j == 0) or graph[i][j] == 1:
            continue

        max_prev = -1

        # 위쪽 칸 (i - 1, j)에서 내려오는 경우
        if i > 0 and dp[i - 1][j] != -1:
            max_prev = max(max_prev, dp[i - 1][j])

        # 왼쪽 칸 (i, j - 1)에서 오른쪽으로 이동하는 경우
        if j > 0 and dp[i][j - 1] != -1:
            if dp[i][j - 1] > max_prev:
                max_prev = max(max_prev, dp[i][j - 1])

        # 둘 중 하나라도 도달 가능한 경로가 있다면 갱신
        if max_prev != -1:
            current_gold = 1 if graph[i][j] == 2 else 0
            dp[i][j] = max_prev + current_gold

result:int = dp[N - 1][M - 1]
print(result if result != -1 else 0)