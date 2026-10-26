# 링크 : https://jungol.co.kr/problem/1295
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
T:int = int(input().rstrip())
A:list = list(map(int, input().split()))

for i in range(T):
    result = binary_search(L, A[i]) + 1
    print(result)