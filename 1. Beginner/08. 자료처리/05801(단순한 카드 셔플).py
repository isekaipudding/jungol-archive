# 링크 : https://jungol.co.kr/problem/5801
import sys
from collections import deque

input = sys.stdin.readline

N:int = int(input().rstrip())

queue:deque = deque([i for i in range(1, N + 1, 1)])

queue.rotate(1)

result:list = []

while queue :
    queue.rotate(-1)
    result.append(queue.popleft())

print(*result)