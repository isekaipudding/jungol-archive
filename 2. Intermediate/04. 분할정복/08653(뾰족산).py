# 링크 : https://jungol.co.kr/problem/8653
import sys

input = sys.stdin.readline

def binary_search(array:list, target:int) -> int :
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

N, Q = map(int, input().split())
H:list = list(map(int, input().split()))

T:int = -1
MAX = max(H)

for index in range(len(H)):
    if H[index] == MAX:
        T = index
        break

H1, H2 = H[:T+1:1], H[T+1::]
H2.sort()

for _ in range(Q):
    x:int = int(input().rstrip())
    
    index1 = binary_search(H1, x)
    if 0 <= index1 < T:
        print("L")
        continue
    if index1 == T:
        print("T")
        continue
    
    index2 = binary_search(H2, x)
    if index2 != -1:
        print("R")
        continue
    
    print("N")