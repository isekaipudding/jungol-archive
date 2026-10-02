# 링크 : https://jungol.co.kr/problem/5932
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())

L:list = [[] for _ in range(2)]
L[0] = [i for i in range(1, N + 1, 1)]
L[1] = [i for i in range(N, 0, -1)]

for i in range(N) :
    print(*L[i % 2])