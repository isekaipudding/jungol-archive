# 링크 : https://jungol.co.kr/problem/1871
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())
A:list = [int(input().rstrip()) for _ in range(N)]

dp:list = [1] * N

# 점화식
for i in range(N):
    for j in range(i):
        if A[j] < A[i]:
            dp[i] = max(dp[i], dp[j] + 1)

print(N - max(dp))