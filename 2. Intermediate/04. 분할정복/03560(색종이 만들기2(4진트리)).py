# 링크 : https://jungol.co.kr/problem/3560
import sys

sys.setrecursionlimit(1 << 20)
input = sys.stdin.readline

def dfs(row, col, size):
    color = graph[row][col]
    
    for r in range(row, row + size):
        for c in range(col, col + size):
            if graph[r][c] != color:
                half = size >> 1
                
                return "X" + dfs(row, col, half) \
                           + dfs(row, col + half, half) \
                           + dfs(row + half, col, half) \
                           + dfs(row + half, col + half, half)
    
    return str(color)

N:int = int(input().rstrip())
graph:list = [list(map(int, input().split())) for _ in range(N)]

print(dfs(0, 0, N))