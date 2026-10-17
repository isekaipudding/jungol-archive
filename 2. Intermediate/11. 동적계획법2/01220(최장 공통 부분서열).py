# 링크 : https://jungol.co.kr/problem/1220
import sys

input = sys.stdin.readline

A:str = input().rstrip()
B:str = input().rstrip()

size_A:int = len(A)
size_B:int = len(B)

dp:list = [[0] * (size_B + 1) for _ in range(size_A + 1)]

# 점화식
for i in range(1, size_A + 1, 1):
    char_A = A[i - 1]
    for j in range(1, size_B + 1, 1):
        if char_A == B[j - 1]:
            dp[i][j] = dp[i - 1][j - 1] + 1
        else:
            dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

print(dp[size_A][size_B])