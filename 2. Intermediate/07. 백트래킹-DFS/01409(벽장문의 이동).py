# 링크 : https://jungol.co.kr/problem/1409
import sys

sys.setrecursionlimit(1 << 20)
input = sys.stdin.readline

def dfs(index:int, current_o1:int, current_o2:int) -> int:
    # 모든 질의를 다 처리한 경우
    if index == M:
        return 0

    # 이미 계산된 상태라면 캐시 반환
    if dp[index][current_o1][current_o2] != -1:
        return dp[index][current_o1][current_o2]

    target:int = queries[index]

    # o1을 target으로 이동
    cost1:int = abs(current_o1 - target) + dfs(index + 1, target, current_o2)

    # o2를 target으로 이동
    cost2:int = abs(current_o2 - target) + dfs(index + 1, current_o1, target)

    dp[index][current_o1][current_o2] = min(cost1, cost2)
    return dp[index][current_o1][current_o2]

N:int = int(input().rstrip())
o1, o2 = map(int, input().split())
M:int = int(input().rstrip())
queries:list = [int(input().rstrip()) for _ in range(M)]

# 3차원 DP 캐시 테이블 dp[index][o1][o2] (-1은 미방문)
dp:list = [[[-1] * (N + 1) for _ in range(N + 1)] for _ in range(M)]

print(dfs(0, o1, o2))