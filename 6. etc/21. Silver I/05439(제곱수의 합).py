# 링크 : https://jungol.co.kr/problem/5439
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())

if N == 0:
    print(0)
    sys.exit(0)

dp:list = [i for i in range(N + 1)]

for i in range(1, N + 1, 1):
    j = 1
    while j * j <= i:
        sq = j * j
        if dp[i] > dp[i - sq] + 1:
            dp[i] = dp[i - sq] + 1
        j += 1

print(dp[N])