# 링크 : https://jungol.co.kr/problem/4518
import sys

input = sys.stdin.readline

N, K = map(int, input().split())

min_required = K * (K + 1) // 2

if N < min_required:
    print(-1)
else:
    rem = (N - min_required) % K
    if rem:
        print(K)
    else:
        print(K - 1)