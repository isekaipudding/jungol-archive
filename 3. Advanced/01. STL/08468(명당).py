# 링크 : https://jungol.co.kr/problem/8468
import sys
from collections import deque

input = sys.stdin.readline

N, K = map(int, input().split())
L:list = list(map(int, input().split()))

max_dq = deque()
min_dq = deque()

left = 0
result = 0

for right in range(N):
    value = L[right]
    
    # 1. max_dq 갱신
    while max_dq and max_dq[-1][0] <= value:
        max_dq.pop()
    max_dq.append((value, right))
    
    # 2. min_dq 갱신
    while min_dq and min_dq[-1][0] >= value:
        min_dq.pop()
    min_dq.append((value, right))
    
    # 3. 최대-최소 차이가 K를 초과하면 left 포인터를 전진
    while max_dq[0][0] - min_dq[0][0] > K:
        left += 1
        
        # 범위를 벗어난 원소 제거
        if max_dq[0][1] < left:
            max_dq.popleft()
        if min_dq[0][1] < left:
            min_dq.popleft()
    
    # 4. 현재 유효한 길이 갱신
    result = max(result, right - left + 1)

print(result)