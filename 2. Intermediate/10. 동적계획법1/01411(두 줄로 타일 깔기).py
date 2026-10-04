# 링크 : https://jungol.co.kr/problem/1411
import sys

input = sys.stdin.readline

MOD = 20100529

N:int = int(input().rstrip())

dp:list = [0 for _ in range(N + 1)]

# 초기식
dp[0], dp[1] = 1, 1

# 점화식
for i in range(2, N + 1, 1) :
    dp[i] = (dp[i-1] + 2 * dp[i-2]) % MOD

print(dp[N])