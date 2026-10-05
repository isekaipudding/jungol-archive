# 링크 : https://jungol.co.kr/problem/5461
import sys
import math

input = sys.stdin.readline

# limit(최댓값)을 기준으로 그룹을 나누었을 때, M개 이하로 나누어지는지 검증
def check(limit):
    group_count = 1
    current_sum = 0
    
    for num in L:
        # 현재 그룹에 구슬을 더 넣었을 때 limit을 초과하면 새로운 그룹 생성
        if current_sum + num > limit:
            group_count += 1
            current_sum = num
        else:
            current_sum += num
            
    # 만들어진 그룹의 수가 M개 이하이면 성공 (limit이 넉넉하다는 뜻)
    return group_count <= M

def parametric_search():
    # 수학적 애드혹(제 아이디어입니다.)
    # lo 선별 조건
    # 1. 배열의 최댓값보다는 커야 한다.
    # 2. 쪼개진 그룹의 평균(ceil(총합 / M))보다는 무조건 커야 한다.
    lo = max(max_marble, math.ceil(total_sum / M))
    hi = total_sum
    best = hi

    while lo <= hi:
        mid = (lo + hi) // 2
        
        if check(mid):
            best = mid
            hi = mid - 1 # 더 작은 최댓값(limit)도 가능한지 탐색
        else:
            lo = mid + 1 # 불가능하므로 최댓값(limit)을 늘려야 함

    return best

N, M = map(int, input().split())
L:list = list(map(int, input().split()))

total_sum:int = sum(L)
max_marble:int = max(L)

result:int = parametric_search()
print(result)