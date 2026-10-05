# 링크 : https://jungol.co.kr/problem/1309
import sys

input = sys.stdin.readline

def dfs(n:int) :
    if n == 1 :
        print("1! = 1")
        return 1
    print(f"{n}! = {n} * {n-1}!")
    return n * dfs(n-1)

N:int = int(input().rstrip())
print(dfs(N))