# 링크 : https://jungol.co.kr/problem/3522
import sys

input = sys.stdin.readline

MOD = 1_000_000_007

N:int = int(input().rstrip())

dp:list = [0 for _ in range(N + 1)]

# 초기식
dp[0], dp[1] = 0, 1

# 점화식
for i in range(2, N+1, 1) :
    dp[i] = (dp[i-1] + dp[i-2]) % MOD

print(dp[N])