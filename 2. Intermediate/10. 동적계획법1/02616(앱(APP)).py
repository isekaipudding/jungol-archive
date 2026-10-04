# 링크 : https://jungol.co.kr/problem/2616
import sys

input = sys.stdin.readline

N, M = map(int, input().split())
memory:list = list(map(int, input().split()))
cost:list = list(map(int, input().split()))

# 앱을 모두 비활성화했을 때의 최대 비용
MAX = sum(cost)

dp:list = [0 for _ in range(MAX + 1)]

# 0-1 배낭 문제(Knapsack Problem) 점화식
for i in range(N):
    m = memory[i]
    c = cost[i]

    # 현재 앱을 한 번만 비활성화할 수 있으므로 뒤에서부터 앞으로(역순) 갱신
    for j in range(MAX, c - 1, -1):
        dp[j] = max(dp[j], dp[j - c] + m)

# 0부터 최대 비용까지 탐색하며 처음으로 M 바이트 이상 확보한 순간의 비용 출력
for cost in range(MAX + 1):
    if dp[cost] >= M:
        print(cost)
        break