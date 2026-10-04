# 링크 : https://jungol.co.kr/problem/1520
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())
L:list = [0 for _ in range(N + 1)]
for i in range(1, N + 1, 1):
    L[i] = int(input().rstrip())

dp:list = [0 for _ in range(N + 1)]

if N == 1:
    print(L[0])
    sys.exit(0)
if N == 2:
    print(L[0] + L[1])
    sys.exit(0)

# 초기식
dp[0], dp[1], dp[2] = 0, L[1], L[1] + L[2]

# 점화식
for i in range(3, N + 1, 1):
    dp[i] = L[i] + max(dp[i-2], L[i-1] + dp[i-3])

print(dp[N])