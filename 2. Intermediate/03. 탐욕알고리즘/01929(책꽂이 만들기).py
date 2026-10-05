# 링크 : https://jungol.co.kr/problem/1929
import sys
import heapq

input = sys.stdin.readline

N:int = int(input().rstrip())
heap:list = []

for _ in range(N):
    heap.append(int(input().rstrip()))

heapq.heapify(heap)

result:int = 0
for _ in range(N - 1):
    a:int = heapq.heappop(heap)
    b:int = heapq.heappop(heap)
    c:int = a + b
    
    result += c
    heapq.heappush(heap, c)

print(result)