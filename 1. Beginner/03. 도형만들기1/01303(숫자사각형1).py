# 링크 : https://jungol.co.kr/problem/1303
import sys

input = sys.stdin.readline

N, M = map(int, input().split())

for i in range(N) :
    for j in range(1, M + 1, 1) :
        print(i * M + j, end="", flush=True)
        if i * M + j != N * M :
            print(" ", end="", flush=True)
    print()