# 링크 : https://jungol.co.kr/problem/1304
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())

for i in range(1, N + 1, 1) :
    L:list = [i + N * j for j in range(N)]
    print(*L)