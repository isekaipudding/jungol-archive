# 링크 : https://jungol.co.kr/problem/1570
import sys
import heapq

input = sys.stdin.readline

N:int = int(input().rstrip())

max_heap = []
min_heap = []

first_value = int(input().rstrip())
heapq.heappush(max_heap, -first_value)
print(first_value)

for _ in range((N - 1) // 2):
    P, Q = map(int, input().split())
    
    for value in (P, Q):
        # max_heap부터 먼저 채웁니다.
        if len(max_heap) == len(min_heap):
            heapq.heappush(max_heap, -value)
        else:
            heapq.heappush(min_heap, value)
        
        # 2. 왼쪽 그룹의 최댓값이 오른쪽 그룹의 최솟값보다 크면 교환합니다.
        if min_heap and -max_heap[0] > min_heap[0]:
            mx = -heapq.heappop(max_heap)
            mn = heapq.heappop(min_heap)
            
            heapq.heappush(max_heap, -mn)
            heapq.heappush(min_heap, mx)
            
    # 무조건 max_heap의 루트가 중앙값입니다.
    print(-max_heap[0])