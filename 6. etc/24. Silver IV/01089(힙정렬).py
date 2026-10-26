# 링크 : https://jungol.co.kr/problem/1089
import sys
import heapq

input = sys.stdin.readline

N, M = map(int, input().split())
heap = list(map(int, input().split()))

heapq.heapify(heap)

result:list = []

while heap:
    result.append(heapq.heappop(heap))

if M == 2:
    result.reverse()

for number in result:
    print(number)