# 링크 : https://jungol.co.kr/problem/8069
import sys

input = sys.stdin.readline

def binary_search(array:list, target:int) -> tuple:
    lo, hi = 0, len(array) - 1

    while lo <= hi:
        mid:int = (lo + hi) // 2
        if array[mid] == target:
            return (mid)
        elif array[mid] < target:
            lo = mid + 1
        else:
            hi = mid - 1
    
    return (hi, lo)

N, Q = map(int, input().split())
L:list = list(map(int, input().split()))

for _ in range(Q):
    n:int = int(input().rstrip())
    index = binary_search(L, n)
    
    if type(index) == int:
        print(n)
    if type(index) == tuple:
        lo, hi = index
        if lo == -1:
            print(L[hi])
            continue
        if hi == N:
            print(L[lo])
            continue
        
        if n - L[lo] <= L[hi] - n:
            print(L[lo])
        else:
            print(L[hi])