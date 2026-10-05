# 링크 : https://jungol.co.kr/problem/8073
import sys

input = sys.stdin.readline

stack:list = []

N:int = int(input().rstrip())

for _ in range(N):
    query:list = list(map(str, input().split()))
    cmd:str = query[0]
    
    if cmd == "i":
        stack.append(int(query[1]))
    if cmd == "o":
        if stack:
            print(stack.pop())
        else:
            print("empty")
    if cmd == "c":
        print(len(stack))