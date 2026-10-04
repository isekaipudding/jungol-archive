# 링크 : https://jungol.co.kr/problem/1077
import sys

input = sys.stdin.readline

N, max_weight = map(int, input().split())
weights:list = [0 for _ in range(N)]
values:list = [0 for _ in range(N)]

for i in range(N):
    weights[i], values[i] = map(int, input().split())

dp:list = [0 for _ in range(max_weight + 1)]

# 초기식
dp[0] = 0

# 점화식
for i in range(N):
    for w in range(weights[i], max_weight + 1):
        dp[w] = max(dp[w], dp[w - weights[i]] + values[i])

print(dp[max_weight])