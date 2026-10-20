# 링크 : https://jungol.co.kr/problem/2913
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())
A:list = list(map(int, input().split()))
B:list = list(map(int, input().split()))

# next_dp[j] : i + 1번째 행의 결과
# curr_dp[j] : 현재 i번째 행의 결과
next_dp = [0] * (N + 1)
curr_dp = [0] * (N + 1)

# i와 j를 뒤에서부터 역방향으로 채워나감
for i in range(N - 1, -1, -1):
    a_value = A[i]
    for j in range(N - 1, -1, -1):
        # 1. 왼쪽 버리기 vs 둘 다 버리기 중 최댓값
        result = max(next_dp[j], next_dp[j + 1])
        
        # 2. 오른쪽 카드 버리기(A[i] > B[j]인 경우)
        if a_value > B[j]:
            result = max(result, curr_dp[j + 1] + B[j])
        curr_dp[j] = result
        
    next_dp[:] = curr_dp

print(curr_dp[0])