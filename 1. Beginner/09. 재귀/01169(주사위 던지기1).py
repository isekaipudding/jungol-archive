# 링크 : https://jungol.co.kr/problem/1169
import sys

input = sys.stdin.readline

LIMIT = 6

def dfs1(depth:int, result:list) -> None :
    if depth >= N :
        print(*result)
        return
    
    for i in range(1, LIMIT + 1, 1) :
        dfs1(depth + 1, result + [i])
    
    return

def dfs2(depth:int, index:int, result:list) :
    if depth >= N :
        print(*result)
        return
    
    for i in range(index, LIMIT + 1, 1) :
        dfs2(depth + 1, i, result + [i])
    
    return

def dfs3(depth:int, index:int, result:list) :
    if depth >= N :
        print(*result)
        return
    
    for i in range(1, LIMIT + 1, 1) :
        if i in result :
            continue
        dfs3(depth + 1, i, result + [i])
    
    return

N, T = map(int, input().split())

if T == 1 :
    dfs1(0, [])
if T == 2 :
    dfs2(0, 1, [])
if T == 3 :
    dfs3(0, 1, [])