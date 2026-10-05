# 링크 : https://jungol.co.kr/problem/1102
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())
stack:list = []

for _ in range(N) :
    query:list = list(map(str, input().split()))
    cmd:str = query[0]
    
    if cmd == "i" :
        a:int = int(query[1])
        stack.append(a)
    if cmd == "o" :
        if stack :
            print(stack.pop())
        else :
            print("empty")
    if cmd == "c" :
        print(len(stack))