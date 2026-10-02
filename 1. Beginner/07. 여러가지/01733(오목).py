# 링크 : https://jungol.co.kr/problem/1733
import sys

input = sys.stdin.readline

LIMIT = 19

def dfs(depth:int, row:int, col:int, number:int, status:int):
    if depth:
        if not check_graph_range(row, col):
            if depth == 5:
                return True
            return False
        if depth < 5 and graph[row][col] != number:
            return False
        if depth == 5 and graph[row][col] != number:
            return True
        
        return dfs(depth + 1, row + status // 2, col + status % 2, number, status)
    
    a:bool = dfs(depth + 1, row, col + 1, number, 1) # 가로 방향 진행
    if check_graph_range(row, col - 1):
        if graph[row][col] == graph[row][col - 1]:
            a = False
    b:bool = dfs(depth + 1, row + 1, col, number, 2) # 세로 방향 진행
    if check_graph_range(row - 1, col):
        if graph[row][col] == graph[row - 1][col]:
            b = False
    c:bool = dfs(depth + 1, row + 1, col + 1, number, 3) # \ 대각선 방향 진행
    if check_graph_range(row - 1, col - 1):
        if graph[row][col] == graph[row - 1][col - 1]:
            c = False
    d:bool = dfs(depth + 1, row - 1, col + 1, number, -1) # / 대각선 방향 진행
    if check_graph_range(row + 1, col - 1):
        if graph[row][col] == graph[row + 1][col - 1]:
            d = False
    
    return a or b or c or d

def check_graph_range(r, c):
    if 0 <= r < LIMIT and 0 <= c < LIMIT:
        return True
    return False

graph:list = []

for _ in range(LIMIT):
    graph.append(list(map(int, input().split())))

for r in range(LIMIT):
    for c in range(LIMIT):
        N:int = graph[r][c]
        if N:
            if dfs(0, r, c, N, 0):
                print(N)
                print(r + 1, c + 1)
                sys.exit(0)

# 만약 없는 경우 그냥 0 출력하기
print(0)