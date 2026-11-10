# 링크 : https://jungol.co.kr/problem/4735
import sys

input = sys.stdin.readline

T:int = int(input().rstrip())

for _ in range(T):
    Q:int = int(input().rstrip())
    S:set = set()
    for _ in range(Q):
        query:list = list(map(str, input().split()))
        cmd:str = query[0]
        
        if cmd == "insert":
            x:int = int(query[1])
            S.add(x)
        
        if cmd == "erase":
            x:int = int(query[1])
            S.discard(x)
        
        if cmd == "update":
            x, y = int(query[1]), int(query[2])
            if y in S:
                continue
            if x in S:
                S.discard(x)
                S.add(y)
        
        if cmd == "print":
            L:list = sorted(S)
            c:int = int(query[1])
            
            c -= 1 # 1-index -> 0-index
            
            size:int = len(L)
            
            if size:
                if c < size:
                    print(L[c])
                else:
                    print(L[-1])
            else:
                print("empty")