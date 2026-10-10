# 링크 : https://jungol.co.kr/problem/3337
import sys
import heapq

input = sys.stdin.readline

N, k = map(int, input().split())

cashiers:int = min(N, k)

pq:list = [(0, c) for c in range(1, cashiers + 1)]
heapq.heapify(pq)

exit_events:list = []

for _ in range(N):
    member_id, need_time = map(int, input().split())
    
    current_time, current_id = heapq.heappop(pq)
    
    finish_time = current_time + need_time
    
    exit_events.append((finish_time, -current_id, member_id))
    
    heapq.heappush(pq, (finish_time, current_id))

exit_events.sort()

result:int = 0

for rank, (_, _, member_id) in enumerate(exit_events, start=1):
    result += rank * member_id

print(result)