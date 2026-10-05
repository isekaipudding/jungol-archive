# 링크 : https://jungol.co.kr/problem/8566
import sys
import heapq

input = sys.stdin.readline

N, P = map(int, input().split())
L:list = list(map(int, input().split()))

result:list = [-1 for _ in range(N)]
heap:list = []
S:int = 0

for i in range(N):
    heapq.heappush(heap, L[i])
    S += L[i]
    
    while heap and S - heap[0] >= P:
        S -= heapq.heappop(heap)

    if S >= P:
        result[i] = len(heap)

print(*result)