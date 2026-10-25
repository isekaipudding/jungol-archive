# 링크 : https://jungol.co.kr/problem/2613
import sys
from collections import deque

input = sys.stdin.readline

directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

def bfs(row, col, tomatoes):
    queue = deque()
    # 초기 토마토(1)의 위치를 담습니다.
    for i in range(row): # 행의 수 (row)
        for j in range(col): # 열의 수 (col)
            if tomatoes[i][j] == 1:
                queue.append((i, j))
    
    days = -1 # 시작일을 -1로 설정
    
    while queue:
        days += 1
        for _ in range(len(queue)):
            r, c = queue.popleft()
            
            for dr, dc in directions:
                nr = r + dr
                nc = c + dc
                
                # 범위 체크 및 빈칸(0) 확인
                if 0 <= nr < row and 0 <= nc < col and tomatoes[nr][nc] == 0:
                    tomatoes[nr][nc] = 1  # 토마토로 변환
                    queue.append((nr, nc))
    
    # 모든 빈칸이 토마토로 변환됐는지 확인
    for i in range(row):
        for j in range(col):
            if tomatoes[i][j] == 0: # 여전히 빈칸이 남아 있다면
                return -1
    
    return days

# M(열), N(행) 입력 받기
M, N = map(int, input().split())
tomatoes = []

# N개의 입력 받기
for _ in range(N):
    row = list(map(int, input().split()))
    tomatoes.append(row)

# BFS 실행 및 결과 출력
result = bfs(N, M, tomatoes)
print(result)