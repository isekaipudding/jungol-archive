# 링크 : https://jungol.co.kr/problem/1021
import sys

input = sys.stdin.readline

def dfs(y:int, k:int):
    if not len(L[y]):
        result[y] += k
        return
    
    for a, b in L[y]:
        dfs(a, b * k)

N:int = int(input().rstrip())
M:int = int(input().rstrip())
L:list = [[] for _ in range(N + 1)]
result:list = [0 for _ in range(N + 1)]

for _ in range(M):
    X, Y, K = map(int, input().split())
    L[X].append([Y, K])

dfs(N, 1)

for i in range(1, N + 1, 1):
    if not len(L[i]):
        print(i, result[i])