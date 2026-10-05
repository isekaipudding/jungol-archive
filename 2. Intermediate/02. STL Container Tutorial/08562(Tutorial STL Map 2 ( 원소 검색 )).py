# 링크 : https://jungol.co.kr/problem/8562
import sys

input = sys.stdin.readline

Q:int = int(input().rstrip())

D:dict = dict()
for _ in range(Q):
    query:list = list(map(str, input().split()))
    cmd:str = query[0]
    
    if cmd == "f":
        x:int = int(query[1])
        if x in D:
            print(f"YES {D[x]}")
        else:
            print("NO")
    if cmd == "a":
        x:int = int(query[1])
        if x not in D:
            D[x] = 1
        else:
            D[x] += 1
    if cmd == "c":
        print(len(D.keys()))