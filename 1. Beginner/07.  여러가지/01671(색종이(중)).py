# 링크 : https://jungol.co.kr/problem/1671
import sys

input = sys.stdin.readline

# 101 x 101 격자 그래프로 해결할 수 있습니다.
graph:list = [[0 for _ in range(101)] for _ in range(101)]

N:int = int(input().rstrip())

for _ in range(N) :
    x, y = map(int, input().split())
    
    for r in range(y, y + 10, 1) :
        for c in range(x, x + 10, 1) :
            graph[r][c] = 1

# ㅡ
horizontal:list = [[0 for _ in range(100)] for _ in range(101)]
# ㅣ
vertical:list = [[0 for _ in range(101)] for _ in range(100)]

# 1번째로 (x, y) = (0, 0)에 해당하는 칸의 2개 선분을 확인합니다.
if graph[0][0] ^ graph[1][0] :
    horizontal[1][0] = 1
if graph[0][0] ^ graph[0][1] :
    vertical[0][1] = 1

# 그 다음으로 x >= 1, y = 0의 모든 칸들을 조사합니다.
for x in range(1, 100, 1) :
    if graph[0][x] ^ graph[0][x-1] :
        vertical[0][x] = 1
    if graph[0][x] ^ graph[1][x] :
        horizontal[1][x] = 1
    if graph[0][x] ^ graph[0][x+1] :
        vertical[0][x+1] = 1

# 그 다음으로 x = 0, y >= 1의 모든 칸들을 조사합니다.
for y in range(1, 100, 1) :
    if graph[y][0] ^ graph[y-1][0] :
        horizontal[y][0] = 1
    if graph[y][0] ^ graph[y][1] :
        vertical[y][1] = 1
    if graph[y][0] ^ graph[y+1][0] :
        horizontal[y+1][0] = 1

# 나머지 x >= 1, y >= 1의 모든 칸들을 조사합니다.

for y in range(1, 100, 1) :
    for x in range(1, 100, 1) :
        if graph[y][x] ^ graph[y][x-1] :
            vertical[y][x] = 1
        if graph[y][x] ^ graph[y+1][x] :
            horizontal[y+1][x] = 1
        if graph[y][x] ^ graph[y][x+1] :
            vertical[y][x+1] = 1
        if graph[y][x] ^ graph[y-1][x] :
            horizontal[y][x] = 1

result:int = 0
for r in range(len(horizontal)) :
    result += sum(horizontal[r])
for r in range(len(vertical)) :
    result += sum(vertical[r])

print(result)