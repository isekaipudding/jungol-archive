# 링크 : https://jungol.co.kr/problem/1314
import sys

input = sys.stdin.readline

# 런타임 전처리(캐시 기능)
D:dict = dict()
for i in range(65, 65 + 26, 1) :
    D[i - 65] = chr(i)

N:int = int(input().rstrip())

# 격자 그래프로 해결합니다.
graph:list = [[None for _ in range(N)] for _ in range(N)]

index:int = 0
for c in range(N) :
    if c & 1 :
        for r in range(N-1, -1, -1) :
            graph[r][c] = D[index % 26]
            index += 1
    else :
        for r in range(N) :
            graph[r][c] = D[index % 26]
            index += 1

for r in range(N) :
    print(*graph[r])