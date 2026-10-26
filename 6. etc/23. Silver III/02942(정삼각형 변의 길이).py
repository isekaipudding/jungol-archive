# 링크 : https://jungol.co.kr/problem/2942
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())

if N < 4:
    print(1)
    sys.exit(0)
if N == 4:
    print(2)
    sys.exit(0)

dp:list = [0] * (N + 1)

# 초기식
for i in range(1, 4, 1):
    dp[i] = 1
dp[4] = 2

# 점화식
for i in range(5, N + 1, 1):
    dp[i] = dp[i - 1] + dp[i - 5]

print(dp[N])