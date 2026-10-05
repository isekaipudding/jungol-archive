# 링크 : https://jungol.co.kr/problem/3234
import sys

input = sys.stdin.readline

LIMIT = 3 * 10 ** 9

N:int = int(input().rstrip())

D:dict = dict()

for _ in range(N):
    axis, color = map(int, input().split())
    
    if color not in D:
        D[color] = [-LIMIT, axis, LIMIT]
    else:
        D[color].append(axis)

result:int = 0

for color in D.keys():
    D[color].sort()
    size:int = len(D[color])
    
    if size <= 3:
        continue
    
    for i in range(1, size - 1, 1):
        result += min(D[color][i] - D[color][i-1], D[color][i+1] - D[color][i])

print(result)