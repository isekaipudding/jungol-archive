# 링크 : https://jungol.co.kr/problem/1072
import sys

input = sys.stdin.readline

N, M = map(int, input().split())
L:list = list(map(int, input().split()))

prefix:list = [0 for _ in range(N + 1)]

# 초기식
prefix[0] = 0

# 점화식
for i in range(1, N + 1, 1) :
    prefix[i] = prefix[i-1] + L[i-1]

result:int = -100 * (2 ** 64 - 1)

# 슬라이딩 윈도우
for i in range(M, N + 1, 1) :
    result = max(result, prefix[i] - prefix[i-M])

print(result)