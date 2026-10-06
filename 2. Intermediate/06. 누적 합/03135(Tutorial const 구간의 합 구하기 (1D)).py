# 링크 : https://jungol.co.kr/problem/3135
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())
L:list = list(map(int, input().split()))

prefix:list = [0 for _ in range(N + 1)]

# 초기식
prefix[0] = 0

# 점화식
for i in range(1, N + 1, 1):
    prefix[i] = prefix[i - 1] + L[i - 1]

Q:int = int(input().rstrip())

for _ in range(Q):
    start, end = map(int, input().split())
    result:int = prefix[end] - prefix[start - 1]
    print(result)