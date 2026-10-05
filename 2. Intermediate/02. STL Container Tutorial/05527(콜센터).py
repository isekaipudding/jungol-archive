# 링크 : https://jungol.co.kr/problem/5527
import sys
from collections import deque

input = sys.stdin.readline

N:int = int(input().rstrip())

queue:deque = deque()
total:int = 0

for _ in range(N):
    query:list = list(map(str, input().split()))
    cmd:str = query[0]
    
    if cmd == "call":
        time:int = int(query[1])
        queue.append(time)
        total += time
    if cmd == "wait":
        time:int = int(query[1])
        # 예외 처리
        if time >= total:
            queue.clear()
            total = 0
            continue
        
        total -= time
        
        while time > 0:
            if time >= queue[0]:
                time -= queue.popleft()
            else:
                queue[0] -= time
                time = 0
    if cmd == "check":
        print(f"{len(queue)} people {total} minutes")