# 링크 : https://jungol.co.kr/problem/8587
import sys
import heapq

input = sys.stdin.readline

heap = []

Q:int = int(input().rstrip())

for _ in range(Q):
    query:list = list(map(str, input().split()))
    cmd:str = query[0]
    
    if cmd == "push":
        name, age, blood = query[1], int(query[2]), float(query[3])
        heapq.heappush(heap, (-blood, -age, name))
    if cmd == "pop":
        if heap:
            name = heapq.heappop(heap)[2]
            print(name)