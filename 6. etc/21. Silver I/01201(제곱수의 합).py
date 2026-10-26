# 링크 : https://jungol.co.kr/problem/1201
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())

dp:list = [i for i in range(N + 1)]

for i in range(1, N + 1, 1):
    j = 1
    while j * j <= i:
        sq = j * j
        if dp[i] > dp[i - sq] + 1:
            dp[i] = dp[i - sq] + 1
        j += 1

print(dp[N])