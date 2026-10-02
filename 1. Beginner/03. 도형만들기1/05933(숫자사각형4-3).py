# 링크 : https://jungol.co.kr/problem/5933
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())

for i in range(1, N + 1, 1) :
    L:list = [i * j for j in range(1, N + 1, 1)]
    print(*L)