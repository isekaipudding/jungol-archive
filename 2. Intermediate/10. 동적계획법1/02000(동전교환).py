# 링크 : https://jungol.co.kr/problem/2000
import sys

input = sys.stdin.readline

INF = float('inf')

N:int = int(input().rstrip())
coins:list = list(map(int, input().split()))
coins.sort()
W:int = int(input().rstrip())

dp:list = [INF for _ in range(W + 1)]

# 초기식
dp[0] = 0

# 점화식
for coin in coins:
    for current_W in range(coin, W + 1, 1):
        if dp[current_W - coin] != INF:
            dp[current_W] = min(dp[current_W], dp[current_W - coin] + 1)

if dp[W] == INF:
    print("impossible")
else:
    print(dp[W])