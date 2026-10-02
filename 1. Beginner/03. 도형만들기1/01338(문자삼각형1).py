# 링크 : https://jungol.co.kr/problem/1338
import sys

input = sys.stdin.readline

# 런타임 전처리(캐시 기능)
D:dict = dict()
for i in range(65, 65 + 26, 1) :
    D[i - 65] = chr(i)

N:int = int(input().rstrip())

# 격자 그래프로 해결합니다.
graph:list = [[" " for _ in range(N)] for _ in range(N)]

index:int = 0

for r in range(N) :
    for i in range(0, N-r, 1) :
        graph[r+i][N-1-i] = D[index % 26]
        index += 1
        
for i in range(N) :
    print(*graph[i])