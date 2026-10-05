# 링크 : https://jungol.co.kr/problem/5804
import sys

input = sys.stdin.readline

def parametric_search():
    # 만약 1 3 5 7인 경우 lo는 1이 아닌 2가 됩니다.
    lo = min(L[i+1] - L[i] for i in range(N-1))
    # 만약 1 3 5 7이고 K = 3인 경우 아무리 생각해도 (7-1) // (3-1) = 3보다 더 큰 정답은 존재하지 않아요.
    hi = (L[-1] - L[0]) // (K - 1)
    best = lo
    
    while lo <= hi:
        mid = (lo + hi) // 2
        
        # 여기에 그리디 알고리즘을 적용합니다.
        # 무조건 첫 나무를 심는 것이 이득입니다.
        count = 1
        last_planted = L[0]
        
        for i in range(1, N, 1):
            if L[i] - last_planted >= mid:
                count += 1
                last_planted = L[i]
        
        # 만약 K그루 이상 심었으면 더 넓혀도 되는지 확인합니다.
        if count >= K:
            best = mid
            lo = mid + 1
        # 만약 K그루 이상 못 심으면 너무 넓으니 좁혀봅시다.
        else:
            hi = mid - 1
    
    return best

N, K = map(int, input().split())

L:list = [0 for _ in range(N)]

for i in range(N):
    x:int = int(input().rstrip())
    L[i] = x

L.sort()

result:int = parametric_search()
print(result)