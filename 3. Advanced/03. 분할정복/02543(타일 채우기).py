# 링크 : https://jungol.co.kr/problem/2543
import sys

sys.setrecursionlimit(1 << 20)
input = sys.stdin.readline

# tr는 top-row, tc는 top-col(현재 탐색 영역의 맨 왼쪽 위 좌표)
# size는 현재 탐색 영역의 한 변의 길이
# hr는 hole-row, hc는 hole-col(현재 영역에서 '구멍' 역할을 하는 곳의 좌표)
def dfs(tr, tc, size, hr, hc):
    # 크기가 1이 되면 더 이상 타일을 깔 수 없으므로 종료
    if size == 1:
        return
    
    half = size >> 1
    
    # 현재 영역의 정중앙을 가르는 십자가의 기준점 (우측 하단 사분면의 시작점)
    cr = tr + half
    cc = tc + half
    
    # 1사분면(Top-Left)에 구멍이 있는 경우
    if hr < cr and hc < cc:
        # Type 1 타일 (1사분면이 뚫려있는 L자)을 정중앙에 배치
        graph[cr-1][cc] = 1 # 2사분면
        graph[cr][cc-1] = 1 # 3사분면
        graph[cr][cc] = 1   # 4사분면
        
        # 4개의 사분면으로 각각 분할 정복 시작
        # (각 사분면에 새로 생긴 타일 조각을 새로운 구멍 좌표로 넘겨줍니다)
        dfs(tr, tc, half, hr, hc)   # 1사분면 (원래 구멍)
        dfs(tr, cc, half, cr-1, cc) # 2사분면 (새 구멍)
        dfs(cr, tc, half, cr, cc-1) # 3사분면 (새 구멍)
        dfs(cr, cc, half, cr, cc)   # 4사분면 (새 구멍)
        
    # 2사분면(Top-Right)에 구멍이 있는 경우
    elif hr < cr and hc >= cc:
        # Type 2 타일 (2사분면이 뚫려있는 L자)을 정중앙에 배치
        graph[cr-1][cc-1] = 2 # 1사분면
        graph[cr][cc-1] = 2   # 3사분면
        graph[cr][cc] = 2     # 4사분면
        
        dfs(tr, tc, half, cr-1, cc-1)
        dfs(tr, cc, half, hr, hc)
        dfs(cr, tc, half, cr, cc-1)
        dfs(cr, cc, half, cr, cc)
        
    # 3사분면(Bottom-Left)에 구멍이 있는 경우
    elif hr >= cr and hc < cc:
        # Type 3 타일 (3사분면이 뚫려있는 L자)을 정중앙에 배치
        graph[cr-1][cc-1] = 3 # 1사분면
        graph[cr-1][cc] = 3   # 2사분면
        graph[cr][cc] = 3     # 4사분면
        
        dfs(tr, tc, half, cr-1, cc-1)
        dfs(tr, cc, half, cr-1, cc)
        dfs(cr, tc, half, hr, hc)
        dfs(cr, cc, half, cr, cc)
        
    # 4사분면(Bottom-Right)에 구멍이 있는 경우
    else:
        # Type 4 타일 (4사분면이 뚫려있는 L자)을 정중앙에 배치
        graph[cr-1][cc-1] = 4 # 1사분면
        graph[cr-1][cc] = 4   # 2사분면
        graph[cr][cc-1] = 4   # 3사분면
        
        dfs(tr, tc, half, cr-1, cc-1)
        dfs(tr, cc, half, cr-1, cc)
        dfs(cr, tc, half, cr, cc-1)
        dfs(cr, cc, half, hr, hc)

N:int = int(input().rstrip())
X, Y = map(int, input().split())

# N x N 크기의 빈 화장실 바닥(초기값 0)
graph:list = [[0 for _ in range(N)] for _ in range(N)]

# 최초 전체 영역을 대상으로 시작(구멍은 X, Y)
dfs(0, 0, N, X, Y)

# 완성된 바닥 출력
for row in graph:
    print(*row)