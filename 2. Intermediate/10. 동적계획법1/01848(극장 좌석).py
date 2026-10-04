# 링크 : https://jungol.co.kr/problem/1848
import sys

input = sys.stdin.readline

# 런타임 전처리
LIMIT = 40

dp:list = [0 for _ in range(LIMIT + 1)]

# 초기식
dp[0], dp[1] = 1, 1

# 점화식
for i in range(2, LIMIT + 1, 1):
    dp[i] = dp[i-1] + dp[i-2]

N:int = int(input().rstrip())
M:int = int(input().rstrip())

L1:list = []
for _ in range(M):
    L1.append(int(input().rstrip()))

L2:list = []

current:int = 0

for i in range(1, N + 1, 1):
    if i in L1:
        L2.append(current)
        current = 0
    else:
        current += 1

L2.append(current)

result:int = 1

for n in L2:
    result *= dp[n]

print(result)