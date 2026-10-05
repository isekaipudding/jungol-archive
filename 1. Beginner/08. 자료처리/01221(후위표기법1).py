# 링크 : https://jungol.co.kr/problem/1221
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())
L:list = list(map(str, input().split()))

stack:list = []

for i in range(N) :
    try :
        K:int = int(L[i])
        stack.append(K)
    except :
        cmd:str = L[i]
        b:int = stack.pop()
        a:int = stack.pop()
        
        if cmd == "+" :
            stack.append(a + b)
        if cmd == "-" :
            stack.append(a - b)
        if cmd == "*" :
            stack.append(a * b)
        if cmd == "/" :
            stack.append(a // b)

result:int = stack[-1]
print(result)