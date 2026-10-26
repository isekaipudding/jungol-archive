# 링크 : https://jungol.co.kr/problem/1190
import sys
import heapq

input = sys.stdin.readline

N:int = int(input().rstrip())
heap:list = list(map(int, input().split()))

heapq.heapify(heap)

result:int = 0
for _ in range(N - 1):
    a:int = heapq.heappop(heap)
    b:int = heapq.heappop(heap)
    c:int = a + b
    
    result += c
    heapq.heappush(heap, c)

print(result)