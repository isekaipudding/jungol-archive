# 링크 : https://jungol.co.kr/problem/1428
import sys

input = sys.stdin.readline

A, B, C, W = map(int, input().split())

dp = [float('inf')] * (W + 1)

# 초기식
dp[0] = 0

# 점화식
for coin in (A, B, C):
    for i in range(coin, W + 1):
        if dp[i - coin] + 1 < dp[i]:
            dp[i] = dp[i - coin] + 1

print(dp[W])