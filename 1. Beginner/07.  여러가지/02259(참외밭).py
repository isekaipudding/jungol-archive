# 링크 : https://jungol.co.kr/problem/2259
import sys

input = sys.stdin.readline

# 신발끈의 공식
def area(size:int, L:list) -> int :
    result:int = 0
    for index in range(size) :
        result += L[index][0] * L[index + 1][1] - L[index][1] * L[index + 1][0]
    return abs(result // 2)

N:int = int(input().rstrip())

points:list = [(0, 0)]

x, y = 0, 0
for _ in range(6) :
    query:list = list(map(int, input().split()))
    cmd:int = query[0]
    move:int = query[1]
    
    if cmd == 1 :
        x += move
    if cmd == 2 :
        x -= move
    if cmd == 3 :
        y -= move
    if cmd == 4 :
        y += move
    
    points.append((x, y))

result:int = area(6, points)

print(N * result)