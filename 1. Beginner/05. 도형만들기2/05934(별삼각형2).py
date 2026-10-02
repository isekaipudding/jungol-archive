# 링크 : https://jungol.co.kr/problem/5934
import sys

input = sys.stdin.readline

def dfs1(count:int) :
    if count <= 1 :
        return
    result:str = " " * ((N + 1) // 2 - count) + "*" * count
    print(result)
    dfs1(count - 1)

def dfs2(count:int) :
    if count > (N + 1) // 2 :
        return
    result:str = " " * (N // 2) + "*" * count
    print(result)
    dfs2(count + 1)

N:int = int(input().rstrip())

if not (1 <= N <= 100) or not N & 1 :
    print("INPUT ERROR!")
    sys.exit(0)

dfs1((N + 1) // 2)
dfs2(1)