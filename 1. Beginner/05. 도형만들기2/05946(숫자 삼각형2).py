# 링크 : https://jungol.co.kr/problem/5946
import sys

input = sys.stdin.readline

def dfs(count:int) :
    if count >= N :
        return
    result:str = "  " * count + (str(count) + " ") * (2 * N - 1 - 2 * count)
    print(result)
    dfs(count + 1)

N:int = int(input().rstrip())

if not (1 <= N <= 50) or not N & 1 :
    print("INPUT ERROR!")
    sys.exit(0)

dfs(0)