# 링크 : https://jungol.co.kr/problem/1175
import sys

input = sys.stdin.readline

LIMIT = 6

def dfs(depth:int, result:list) -> None :
    if depth >= N :
        if sum(result) == M :
            print(*result)
        return
    
    for i in range(1, LIMIT + 1, 1) :
        dfs(depth + 1, result + [i])
    
    return

N, M = map(int, input().split())

dfs(0, [])