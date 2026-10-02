# 링크 : https://jungol.co.kr/problem/3427
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())
line:str = input().rstrip()

color:str = ""
current:int = 0

stack:list = []

for ball in line :
    if color == "" :
        color = ball
        current = 1
        continue
    if color == ball :
        current += 1
    else :
        color = ball
        stack.append(current)
        current = 1

stack.append(current)

size:int = len(stack)

if size & 1 :
    first, last = stack[0], stack[-1]
    even, odd = 0, 0
    for i in range(2, size - 1, 2) :
        even += stack[i]
    for i in range(1, size - 1, 2) :
        odd += stack[i]
    
    result:int = min(odd, even + min(first, last))
    
    print(result)

else :
    even, odd = 0, 0
    for i in range(2, size - 1, 2) :
        even += stack[i]
    for i in range(1, size - 1, 2) :
        odd += stack[i]
    
    result:int = min(odd, even)
    
    print(result)