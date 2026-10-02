# 링크 : https://jungol.co.kr/problem/1009
import sys

input = sys.stdin.readline

while True :
    N:str = input().rstrip()
    
    if N == "0" :
        break
    
    result1:str = ""
    status:bool = False
    size:int = len(N)
    
    for i in range(size-1, -1, -1) :
        if N[i] == "0" and not status :
            continue
        result1 += N[i]
        status = True
        
    result2:int = 0
    
    size = len(result1)
    
    for i in range(0, size, 1) :
        result2 += int(result1[i])
        
    print(result1, result2)