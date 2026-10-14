# 링크 : https://jungol.co.kr/problem/8605
import sys

input = sys.stdin.readline

N, S = map(int, input().split())
A:list = list(map(int, input().split()))

prefix:list = [0] * (N + 1)
for i in range(N):
    prefix[i + 1] = prefix[i] + A[i]

K:int = N >> 1

# 짝수인 경우
result:int = 2 * ((prefix[N] - prefix[N - K]) - prefix[K]) + S

# 홀수인 경우 결과값 변경
if N & 1:
    result = 2 * ((prefix[N] - prefix[N - (K + 1)]) - prefix[K]) - S

print(result)