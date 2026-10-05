# 링크 : https://jungol.co.kr/problem/2817
import sys

input = sys.stdin.readline

LIMIT = 6

def dfs(depth:int, index:int, result:list) -> None :
    if depth == LIMIT :
        print(*result)
        return
    
    for i in range(index, size, 1) :
        if L[i] in result :
            continue
        dfs(depth + 1, i, result + [L[i]])
    
    return

L:list = list(map(int, input().split()))
K:int = L[0]
size:int = len(L)

dfs(0, 1, [])