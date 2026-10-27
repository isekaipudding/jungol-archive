# 링크 : https://jungol.co.kr/problem/4521
import sys

sys.setrecursionlimit(1 << 20)
input = sys.stdin.readline

# 구현 과정 복잡하고 더럽네요...

def dfs(index:int, current_p:int, current_f:int, current_s:int, current_v:int, current_cost:int, selected:list) -> None:
    global min_cost, best_indices

    # 이미 찾은 최소 비용을 초과하면 탐색 중단
    if current_cost > min_cost:
        return

    # 영양소 충족 시 조기 종료
    # 영양소를 모두 만족하면, 더 추가해 봐야 비용만 늘어나고 사전순으로도 밀리므로 즉시 갱신 후 반환
    if current_p >= mp and current_f >= mf and current_s >= ms and current_v >= mv:
        if current_cost < min_cost:
            min_cost = current_cost
            best_indices = selected[:]
        elif current_cost == min_cost:
            if not best_indices or selected < best_indices:
                best_indices = selected[:]
        return

    # 모든 재료를 탐색한 경우
    if index == N:
        return

    p, f, s, v, c = ingredients[index]

    # index번 식재료를 선택하는 경우(1-based index)
    selected.append(index + 1)
    dfs(index + 1, current_p + p, current_f + f, current_s + s, current_v + v, current_cost + c, selected)
    selected.pop()  # 백트래킹 복구

    # index번 식재료를 선택하지 않는 경우
    dfs(index + 1, current_p, current_f, current_s, current_v, current_cost, selected)

N:int = int(input().rstrip())
mp, mf, ms, mv = map(int, input().split())

# 식재료 정보 : (단백질, 지방, 탄수화물, 비타민, 비용)
ingredients:list = [list(map(int, input().split())) for _ in range(N)]

min_cost = float('inf')
best_indices:list = []

# 0번 식재료부터 탐색 시작
dfs(0, 0, 0, 0, 0, 0, [])

# 결과 출력
if min_cost == float('inf'):
    print(-1)
else:
    print(min_cost)
    print(*best_indices)