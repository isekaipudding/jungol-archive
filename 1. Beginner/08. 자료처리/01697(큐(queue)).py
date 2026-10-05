# 링크 : https://jungol.co.kr/problem/1697
import sys
from collections import deque

input = sys.stdin.readline

N:int = int(input().rstrip())
queue:deque = deque()

for _ in range(N) :
    query:list = list(map(str, input().split()))
    cmd:str = query[0]
    
    if cmd == "i" :
        a:int = int(query[1])
        queue.append(a)
    if cmd == "o" :
        if queue :
            print(queue.popleft())
        else :
            print("empty")
    if cmd == "c" :
        print(len(queue))