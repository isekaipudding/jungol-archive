# 링크 : https://jungol.co.kr/problem/8589
import sys
import heapq

input = sys.stdin.readline

N:int = int(input().rstrip())
L:list = list(map(int, input().split()))

heap:list = []
for n in L:
    heapq.heappush(heap, n)

M:int = int(input().rstrip())
moneys:list = list(map(int, input().split()))

for money in moneys:
    TEMP:int = heapq.heappop(heap)
    heapq.heappush(heap, TEMP + money)

heap.sort()

print(*heap)