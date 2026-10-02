# 링크 : https://jungol.co.kr/problem/1438
import sys

input = sys.stdin.readline

# 100 x 100 격자 그래프로 해결할 수 있습니다.
graph:list = [[0 for _ in range(100)] for _ in range(100)]

N:int = int(input().rstrip())

for _ in range(N) :
    x, y = map(int, input().split())
    
    for r in range(y, y + 10, 1) :
        for c in range(x, x + 10, 1) :
            graph[r][c] = 1

result:int = 0

for r in range(100) :
    result += sum(graph[r])

print(result)