# 링크 : https://jungol.co.kr/problem/4637
import sys

input = sys.stdin.readline

S:set = set()

Q:int = int(input().rstrip())

for _ in range(Q):
    query:list = list(map(str, input().split()))
    cmd:str = query[0]
    
    if cmd == "i":
        N:int = int(query[1])
        S.add(N)
    if cmd == "r":
        N:int = int(query[1])
        S.discard(N)

L:list = list(S)
L.sort()

print(*L)