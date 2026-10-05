# 링크 : https://jungol.co.kr/problem/8654
import sys

input = sys.stdin.readline

def binary_search(array:list, target:int) -> int :
    lo, hi = 0, len(array) - 1
    
    while lo <= hi :
        mid:int = (lo + hi) // 2
        
        if array[mid] <= target :
            lo = mid + 1
        else :
            hi = mid - 1
            
    return hi

N, T = map(int, input().split())
L:list = list(map(int, input().split()))
L.sort()

prefix:list = [0 for _ in range(N + 1)]
for i in range(1, N + 1, 1):
    prefix[i] = prefix[i-1] + L[i-1]

lo_X, hi_X = 0, T
result = hi_X

while lo_X <= hi_X:
    mid_X = (lo_X + hi_X) // 2

    index = binary_search(L, mid_X)
    
    # 누적합 + 수학적 애드혹(어차피 index 이후의 min(L[i], X)가 항상 X라는 것을 이용합니다.)
    # 이렇게 하면 굳이 더 탐색하지 않아도 O(1) 속도로 금방 계산 끝냅니다.
    total = prefix[index + 1]  + mid_X * (N - (index + 1))
    
    if total >= T:
        result = mid_X
        hi_X = mid_X - 1
    else:
        lo_X = mid_X + 1
        
print(result)