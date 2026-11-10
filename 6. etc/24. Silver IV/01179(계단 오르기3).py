# 링크 : https://jungol.co.kr/problem/1179
import sys

input = sys.stdin.readline

MOD = 1_000_000_007

N:int = int(input().rstrip())

size:int = max(3, N + 1)
dp:list = [0] * size

# 초기식
for i in range(3):
    dp[i] = 1

# 점화식
for i in range(3, size, 1):
    dp[i] = (dp[i - 2] + dp[i - 3]) % MOD

print(dp[N])