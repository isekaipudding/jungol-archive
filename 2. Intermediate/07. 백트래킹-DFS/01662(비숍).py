# 링크 : https://jungol.co.kr/problem/1662
import sys

input = sys.stdin.readline

def dfs(d1:int, used_d2_mask:int) -> int:
    """
    d1: 현재 탐색 중인 우상향 대각선 인덱스 (r + c)
    used_d2_mask: 현재까지 비숍이 놓인 우하향 대각선(r - c + N - 1)들의 비트 집합
    """
    # 보드의 끝 대각선까지 탐색을 마침
    if d1 >= 2 * N - 1:
        return 0
    
    # 1. 현재 d1 대각선에 비숍을 아예 놓지 않고 다음으로 넘어가는 경우
    # (같은 색상의 칸만 탐색하기 위해 d1 + 2 호출)
    max_bishops = dfs(d1 + 2, used_d2_mask)
    
    # 2. 현재 d1 대각선에 존재하는 유효한 칸 중 '하나'에 비숍을 놓는 경우
    for r, c in d1_groups[d1]:
        d2 = r - c + (N - 1)
        bit = 1 << d2
        
        # 교차하는 우하향 대각선(d2)에 다른 비숍이 없다면 배치 진행
        if not (used_d2_mask & bit):
            max_bishops = max(max_bishops, dfs(d1 + 2, used_d2_mask | bit) + 1)
            
    return max_bishops

N:int = int(input().rstrip())
board:list = [list(map(int, input().split())) for _ in range(N)]

# 1. d1 (우상향 대각선, r + c)을 기준으로 놓을 수 있는 칸들을 그룹화
# d1의 범위는 0 부터 2*N - 2 까지
d1_groups:list = [[] for _ in range(2 * N - 1)]
for r in range(N):
    for c in range(N):
        if board[r][c] == 1:
            d1_groups[r + c].append((r, c))
            
black:int = dfs(0, 0)
white:int = dfs(1, 0)

print(black + white)