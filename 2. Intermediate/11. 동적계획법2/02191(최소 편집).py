# 링크 : https://jungol.co.kr/problem/2191
import sys

input = sys.stdin.readline

N, A = map(str, input().split())
M, B = map(str, input().split())
N, M = int(N), int(M)

# a의 i번째 접두사를 b의 j번째 접두사로 변환하는 최소 횟수
dp:list = [[0] * (M + 1) for _ in range(N + 1)]

# 초기식
for i in range(N + 1):
    dp[i][0] = i
for j in range(M + 1):
    dp[0][j] = j

# 점화식
for i in range(1, N + 1, 1):
    char_A = A[i - 1]
    for j in range(1, M + 1, 1):
        if char_A == B[j - 1]:
            # 문자가 같으면 비용 0
            dp[i][j] = dp[i - 1][j - 1]
        else:
            # 문자가 다르면 삭제, 삽입, 치환 중 최솟값 + 1
            dp[i][j] = 1 + min(
                dp[i - 1][j],    # 삭제
                dp[i][j - 1],    # 삽입
                dp[i - 1][j - 1] # 치환
            )

print(dp[N][M])