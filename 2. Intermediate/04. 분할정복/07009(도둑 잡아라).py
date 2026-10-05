# 링크 : https://jungol.co.kr/problem/7009
import sys

input = sys.stdin.readline

def binary_search(array:list, target:int) -> bool :
    lo, hi = 0, len(array) - 1
    
    while lo <= hi :
        mid:int = (lo + hi) // 2
        
        if array[mid] == target :
            return True
        elif array[mid] < target :
            lo = mid + 1
        else :
            hi = mid - 1
            
    return False

N, Q = map(int, input().split())
L:list = list(map(int, input().split()))
L.sort()

A:list = list(map(int, input().split()))

result:list = []

for a in A:
    if not binary_search(L, a):
        result.append(a)

if result:
    print(*result)
else:
    print(-1)