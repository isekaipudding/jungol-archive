# 링크 : https://jungol.co.kr/problem/4180
import sys

input = sys.stdin.readline

def dfs(depth:int, L:list, index:int):
    if depth >= M:
        print(*L)
        return
    for n in range(index, N + 1, 1):
        dfs(depth + 1, L + [n], n)

N, M = map(int, input().split())

dfs(0, [], 1)