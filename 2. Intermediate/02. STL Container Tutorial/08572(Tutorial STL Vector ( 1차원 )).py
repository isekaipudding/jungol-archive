# 링크 : https://jungol.co.kr/problem/8572
import sys

input = sys.stdin.readline

N, X = map(int, input().split())

vector:list = [X for _ in range(N)]

while True:
    query:list = list(map(str, input().split()))
    cmd:str = query[0]
    
    if cmd == "e":
        break
    if cmd == "i":
        a:int = int(query[1])
        vector.append(a)
    if cmd == "r":
        if vector:
            vector.pop()
    if cmd == "s":
        vector.sort()
    if cmd == "t":
        if vector:
            vector[0], vector[-1] = vector[-1], vector[0]

print(*vector)