# 링크 : https://jungol.co.kr/problem/3603
import sys

input = sys.stdin.readline

# 과거에 백준에 제출했던 소스 코드를 제출합니다.

N:int = int(input().rstrip())
dp:list = list(map(int, input().split()))
L:list = [0, 0] + list(map(int, input().split()))

protocol:list = [0 for _ in range(N)]
host:list = [0 for _ in range(N)]

for i in range(0, 2 * N, 2) :
    host[i // 2] = L[i]
    protocol[i // 2] = L[i+1]

# 이 문제는 바텀 업 트리 dp로 해결 가능합니다.
result:int = 0
for i in range(N-1, 0, -1) :
    if protocol[i] == 0 :
        result += dp[i]
        dp[host[i]] = max(0, dp[host[i]] - dp[i])
    if protocol[i] == 1 :
        dp[host[i]] += dp[i]
    if protocol[i] == 2 :
        dp[host[i]] = max(dp[host[i]], dp[i])

print(result + dp[0])