# 링크 : https://jungol.co.kr/problem/2082
import sys
import heapq

input = sys.stdin.readline

N:int = int(input().rstrip())
L:list = list(map(int, input().split()))

heap = [-item for item in L]
heapq.heapify(heap)

new_heap = [-item for item in heap]
print(*new_heap)

new_heap.sort()
print(*new_heap)