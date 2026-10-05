# 링크 : https://jungol.co.kr/problem/1146
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())
L:list = list(map(int, input().split()))

first_index:int = 0
for _ in range(N-1) :
    MIN = min(L[first_index::])
    
    second_index:int = first_index
    
    for i in range(first_index, N, 1) :
        if L[i] == MIN :
            second_index = i
            break
    
    L[first_index], L[second_index] = L[second_index], L[first_index]
    
    print(*L)
    
    first_index += 1