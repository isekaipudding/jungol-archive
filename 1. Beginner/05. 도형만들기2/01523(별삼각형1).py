# 링크 : https://jungol.co.kr/problem/1523
import sys

input = sys.stdin.readline

def dfs1(count:int) :
    if count > N :
        return
    print("*" * count)
    dfs1(count + 1)

def dfs2(count:int) :
    if count < 1 :
        return
    print("*" * count)
    dfs2(count - 1)

def dfs3(count:int) :
    if count > N :
        return
    result:str = " " * (N - count) + "*" * (2 * count - 1)
    print(result)
    dfs3(count + 1)

N, M = map(int, input().split())

if not (1 <= N <= 100) or not (1 <= M <= 3) :
    print("INPUT ERROR!")
    sys.exit(0)

if M == 1 :
    dfs1(1)
if M == 2 :
    dfs2(N)
if M == 3 :
    dfs3(1)