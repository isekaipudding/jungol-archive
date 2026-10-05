# 링크 : https://jungol.co.kr/problem/3249
import sys

sys.setrecursionlimit(1 << 20)
input = sys.stdin.readline

index = 0
def dfs(row, col, size):
    global index
    
    char = code[index]
    index += 1
    
    if char == "X":
        half = size >> 1
        dfs(row, col, half)
        dfs(row, col + half, half)
        dfs(row + half, col, half)
        dfs(row + half, col + half, half)
    else:
        color = int(char)
        for r in range(row, row + size):
            for c in range(col, col + size):
                graph[r][c] = color

N:int = int(input().rstrip())
code:str = input().rstrip()

graph:list = [[-1 for _ in range(N)] for _ in range(N)]

dfs(0, 0, N)

print(N)
for r in range(N):
    print(*graph[r])