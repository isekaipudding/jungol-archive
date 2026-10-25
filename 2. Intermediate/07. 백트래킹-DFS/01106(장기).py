# 링크 : https://jungol.co.kr/problem/1106
import sys

sys.setrecursionlimit(1 << 20)
input = sys.stdin.readline

dr = (
    -2, -2,
    -1, -1,
    1, 1,
    2, 2
)
dc = (
    -1, 1,
    -2, 2,
    -2, 2,
    -1, 1
)

def dfs(r:int, c:int, count:int):
    global min_moves
    
    # 이미 찾은 타겟까지의 최소 이동 횟수보다 같거나 크면 탐색 중단
    expected_remains = max(abs(r - S) // 2, abs(c - K) // 2)
    if count + expected_remains >= min_moves:
        return
        
    # 현재 칸에 도달한 기존 최소 횟수보다 크거나 같다면 더 이상 탐색 중단
    if count >= distance[r][c]:
        return
        
    # 현재 칸까지의 최소 이동 횟수 갱신
    distance[r][c] = count

    # 목표 위치(졸)에 도달한 경우 최소 이동 횟수 갱신 후 백트래킹(되돌아가기)
    if r == S and c == K:
        min_moves = min(min_moves, count)
        return

    # 8방향 탐색
    next_moves = []
    for i in range(8):
        nr = r + dr[i]
        nc = c + dc[i]
        if 1 <= nr <= N and 1 <= nc <= M:
            if count + 1 < distance[nr][nc]:
                # (목표까지의 거리 제곱, nr, nc) 튜플로 저장
                dist_sq = (nr - S) ** 2 + (nc - K) ** 2
                next_moves.append((dist_sq, nr, nc))
    
    # 거리가 가까운 순으로 정렬 후 DFS 진입
    next_moves.sort(key=lambda x: x[0])
    for _, nr, nc in next_moves:
        dfs(nr, nc, count + 1)

N, M = map(int, input().split())

R, C, S, K = map(int, input().split())

# 예외 처리
if (R, C) == (S, K):
    print(0)
    sys.exit(0)

# 거리 메모이제이션 배열: 무한대(inf)로 초기화
distance = [[float('inf')] * (M + 1) for _ in range(N + 1)]

# 최소 이동 횟수를 저장할 전역 변수
min_moves = float('inf')

# 백트래킹 시작
dfs(R, C, 0)

result:int = min_moves
print(result)