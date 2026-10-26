# 링크 : https://jungol.co.kr/problem/1058
import sys

input = sys.stdin.readline

N, K = map(int, input().split())
L:list = list(map(int, input().split()))

prefix:list = [0] * (N + 1)

# 초기식
prefix[0] = 0

# 점화식
for i in range(1, N + 1, 1):
    prefix[i] = prefix[i - 1] + L[i - 1]

start, end = 0, K

result:int = -float('inf')

while end < N:
    result = max(
        result,
        prefix[end] - prefix[start]
    )
    start += 1
    end += 1

print(result)