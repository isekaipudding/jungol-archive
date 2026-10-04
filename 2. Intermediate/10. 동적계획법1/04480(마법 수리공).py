# 링크 : https://jungol.co.kr/problem/4480
import sys

input = sys.stdin.readline

N, M, K = map(int, input().split())
C:list = list(map(int, input().split()))

MAX_MAGIC = K + N * M

prev_dp:list = [-1 for _ in range(MAX_MAGIC + 1)]

# 초기식
prev_dp[K] = 0

# 점화식
for i in range(N):
    curr_dp:list = [-1 for _ in range(MAX_MAGIC + 1)]
    cost = C[i]
    
    for j in range(K + i * M + 1):
        if prev_dp[j] != -1:
            if j >= cost:
                curr_dp[j - cost] = max(curr_dp[j - cost], prev_dp[j] + cost)
            curr_dp[j + M] = max(curr_dp[j + M], prev_dp[j])
    prev_dp = curr_dp

print(max(prev_dp))