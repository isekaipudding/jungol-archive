# 링크 : https://jungol.co.kr/problem/1511
import sys

input = sys.stdin.readline

LIMIT = 5000

dp:list = [0] * (LIMIT + 1)

# 초기식
dp[1] = 1

# 점화식
for i in range(2, LIMIT + 1, 1):
    dp[i] = dp[i - 1] + dp[i - 2]

T:int = int(input().rstrip())

for _ in range(T):
    N:int = int(input().rstrip())
    print(dp[N])