# 링크 : https://jungol.co.kr/problem/1031
import sys

input = sys.stdin.readline

LIMIT = 5

graph:list = [[0 for _ in range(LIMIT)] for _ in range(LIMIT)]

for r in range(LIMIT):
    L:list = list(map(int, input().split()))
    for c in range(LIMIT):
        graph[r][c] = L[c]

# 0 ~ LIMIT - 1 : 가로줄 빙고
# LIMIT ~ 2 * LIMIT - 1 : 세로줄 빙고
# 2 * LIMIT ~ 2 * LIMIT + 1 : 대각선 빙고
BINGO:list = [set() for _ in range(2 * LIMIT + 2)]

# 가로줄 채워넣기
for r in range(LIMIT):
    for c in range(LIMIT):
        BINGO[r].add(graph[r][c])

# 세로줄 채워넣기
for c in range(LIMIT):
    for r in range(LIMIT):
        BINGO[LIMIT + c].add(graph[r][c])

# 대각선 채우기
for s in range(LIMIT):
    BINGO[2 * LIMIT].add(graph[s][s]) # \ 대각선
    BINGO[2 * LIMIT + 1].add(graph[s][LIMIT - 1 - s]) # / 대각선

TEMP = [0 for _ in range(2 * LIMIT + 2)]

for i in range(2 * LIMIT + 2):
    TEMP[i] = len(BINGO[i])

check:list = []

for i in range(LIMIT):
    L:list = list(map(int, input().split()))
    for j in range(LIMIT):
        check.append((LIMIT * i + j + 1, L[j]))

for index, value in check:
    for i in range(len(BINGO)):
        BINGO[i].discard(value)
    
    zero_count:int = 0
    for i in range(len(BINGO)):
        if not BINGO[i]:
            zero_count += 1
    
    if zero_count >= 3:
        print(index)
        break