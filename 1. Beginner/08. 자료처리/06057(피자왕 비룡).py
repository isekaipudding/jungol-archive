# 링크 : https://jungol.co.kr/problem/6057
import sys
from collections import deque

input = sys.stdin.readline

P, N = map(int, input().split())

made_pizza:list = [deque() for _ in range(P + 1)]

result:int = 0
for _ in range(N) :
    query:list = list(map(int, input().split()))
    cmd:int = query[0]
    
    if cmd == 0 :
        p, m = query[1], query[2]
        made_pizza[p].append(m)
    if cmd == 1 :
        p:int = query[1]
        if made_pizza[p] :
            result += made_pizza[p].popleft()

print(result)