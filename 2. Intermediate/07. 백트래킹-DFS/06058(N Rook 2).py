# 링크 : https://jungol.co.kr/problem/6058
import sys

sys.setrecursionlimit(1 << 20)
input = sys.stdin.readline

def dfs(r:int, col_mask:int) -> int:
    # 0번 행부터 N-1번 행까지 모든 룩 배치 완료
    if r == N:
        return 1

    total_ways = 0

    # 현재 r번 행의 빈칸 중 아직 사용되지 않은 열 비트마스크
    avail = row_mask[r] & ~col_mask

    # 룩을 놓을 수 있는 열 비트만 펜윅 비트 연산으로 추출하여 전이
    while avail:
        bit = avail & -avail
        avail -= bit
        total_ways += dfs(r + 1, col_mask | bit)

    return total_ways

N:int = int(input().rstrip())
graph:list = [list(''.join(input().split())) for _ in range(N)]

# 각 행(row)에서 룩을 놓을 수 있는 빈칸('.')들의 열 비트마스크 사전 전처리
row_mask:list = [0] * N
for r in range(N):
    for c in range(N):
        if graph[r][c] == '.':
            row_mask[r] |= (1 << c)

# 0번 행, 사용된 열 비트 0에서 백트래킹 시작
print(dfs(0, 0))