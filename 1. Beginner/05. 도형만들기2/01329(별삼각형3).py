# 링크 : https://jungol.co.kr/problem/1329
import sys

input = sys.stdin.readline

def dfs1(count:int) :
    if count >= N :
        return
    result:str = " " * (count // 2) + "*" * count
    print(result)
    dfs1(count + 2)
    
def dfs2(count:int) :
    if count < 1 :
        return
    result:str = " " * (count // 2) + "*" * count
    print(result)
    dfs2(count - 2)

N:int = int(input().rstrip())

if not (1 <= N <= 100) or not N & 1 :
    print("INPUT ERROR!")
    sys.exit(0)

dfs1(1)
print(" " * (N // 2) + "*" * N)
dfs2(N - 2)