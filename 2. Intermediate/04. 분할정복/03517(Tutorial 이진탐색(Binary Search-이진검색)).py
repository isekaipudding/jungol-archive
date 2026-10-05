# 링크 : https://jungol.co.kr/problem/3517
import sys

input = sys.stdin.readline

def binary_search(array:list, target:int) -> bool :
    lo, hi = 0, len(array) - 1
    
    while lo <= hi :
        mid:int = (lo + hi) // 2
        
        if array[mid] == target :
            return mid
        elif array[mid] < target :
            lo = mid + 1
        else :
            hi = mid - 1
            
    return -1

N:int = int(input().rstrip())
L:list = list(map(int, input().split()))
L.sort()

Q:int = int(input().rstrip())
A:list = list(map(int, input().split()))

result:list = [binary_search(L, A[i]) for i in range(Q)]
print(*result)