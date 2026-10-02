# 링크 : https://jungol.co.kr/problem/1339
import sys

input = sys.stdin.readline

# 런타임 전처리(캐시 기능)
D:dict = dict()
for i in range(65, 65 + 26, 1) :
    D[i - 65] = chr(i)

N:int = int(input().rstrip())

if N < 1 or N > 100 or not N & 1 :
    print("INPUT ERROR")
    sys.exit(0)
    
# 격자 그래프
graph:list = [[" " for _ in range(N // 2 + 1)] for _ in range(N)]

index:int = 0

for c in range(N // 2, -1, -1) :
    for r in range(c, N-c, 1) :
        graph[r][c] = D[index % 26]
        index += 1

for i in range(N) :
    print(*graph[i])