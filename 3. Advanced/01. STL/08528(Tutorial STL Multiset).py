# 링크 : https://jungol.co.kr/problem/8528
import sys

input = sys.stdin.readline

D:dict = dict()

Q:int = int(input().rstrip())

for _ in range(Q):
    query:list = list(map(str, input().split()))
    cmd:str = query[0]
    
    if cmd == "i":
        N:int = int(query[1])
        if N not in D:
            D[N] = 1
        else:
            D[N] += 1
    if cmd == "r":
        N:int = int(query[1])
        if N not in D:
            pass
        else:
            if D[N] > 1:
                D[N] -= 1
            else:
                del D[N]
    if cmd == "e":
        N:int = int(query[1])
        if N in D:
            del D[N]

result:list = []

keys:list = sorted(list(D.keys()))

for k in keys:
    result = result + [k for _ in range(D[k])]

print(*result)