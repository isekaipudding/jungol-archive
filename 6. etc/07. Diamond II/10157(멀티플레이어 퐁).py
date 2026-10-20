# 링크 : https://jungol.co.kr/problem/10157
import sys

sys.setrecursionlimit(1 << 20)

input = sys.stdin.readline

# 에디토리얼 : https://googlecodejam.net/2013r2/problems/index.html#analysis-D

INF = 10 ** 250

# 유클리드 애드혹 O(log M)
# 모듈러 M 공간에서 폭 S로 점프할 때, 최초로 구간 [L, R]에 떨어지는 횟수 반환
def first_hit_in_interval(S, M, L, R):
    # 1. 시작하자마자 구간 안에 있는 경우
    if L == 0: return 0
    
    # 2. 보폭이 공간의 절반을 넘으면 역방향 관점으로 차원 뒤집기
    if 2 * S > M: return first_hit_in_interval(M - S, M, M - R, M - L)
    
    # 3. 한 바퀴를 돌기 전에 목표 구간에 착지하는지 확인
    x_min = (L - 1) // S + 1
    if x_min * S <= R: return x_min
    
    # 4. 영원히 도달할 수 없는 경우 (ZeroDivisionError 방지)
    if M % S == 0: return INF
    
    # 5. 유클리드 호제법: 관점을 x(점프)에서 y(바퀴 수)로 뒤집어 차원 붕괴
    y = first_hit_in_interval(M % S, S, (-R) % S, (-L) % S)
    
    # 6. 하위 재귀에서 도달 불가(INF) 판정이 났을 경우
    if y >= INF: return INF
    
    # 7. 도출된 바퀴 수(y)를 바탕으로 정답 점프 횟수(x) 복원
    return (y * M + L + S - 1) // S

T:int = int(input().rstrip())

for number in range(1, T + 1, 1):
    A, B = map(int, input().split())
    N, M = map(int, input().split())
    V, W = map(int, input().split())
    Y, X, VY, VX = map(int, input().split())
    
    # 예외 처리: 공이 수직으로만 움직이면 절대 벽에 닿지 않음
    if VX == 0:
        print(f"Case #{number}: DRAW")
        continue
    
    original_L = "LEFT"
    original_R = "RIGHT"
    
    # 대칭 이동 1: 공이 왼쪽으로 출발하면, 우주 전체를 좌우로 뒤집어서 우측 출발로 고정
    if VX < 0:
        X = B - X
        VX = -VX
        N, M = M, N
        V, W = W, V
        original_L, original_R = original_R, original_L
        
    # 대칭 이동 2: 공이 아래로 출발하면, 우주 전체를 상하로 뒤집음
    if VY < 0:
        Y = A - Y
        VY = -VY
        
    # 예외 처리: 공이 수평으로만 움직이면 절대 죽음의 구간이 생기지 않음
    if VY == 0:
        print(f"Case #{number}: DRAW")
        continue
        
    # 물리 공간의 정수화 및 모듈러 압축
    M_mod = 2 * A * VX                 # 1차원 원형 트랙의 총 길이
    S = (2 * B * VY) % M_mod           # 공이 반대쪽 벽을 치고 돌아올 때마다(왕복) 이동하는 모듈러 거리
    J = (2 * S) % M_mod                # 한 팀 입장에서, 자기 벽에 공이 돌아올 때마다 이동하는 모듈러 거리
    
    # LEFT 팀의 패배 지점(k_L) 도출
    # 첫 번째 LEFT 벽 타격 시점의 Y축 거리 계산 (수평 이동 거리는 2B - X)
    D0_L = Y * VX + VY * (2 * B - X)
    Z0_L = (2 * D0_L) % M_mod
    
    E_L = V * N * 2 * B               # 패들이 다음 차례까지 최대로 움직일 수 있는 거리
    delta_L = (N * S) % M_mod         # 다음 차례까지 공이 도망가는 거리
    distance_L = min(delta_L, M_mod - delta_L)
    
    if distance_L <= E_L:
        k_L = INF                     # 공이 도망가는 거리보다 패들이 빠르면 영원히 안 죽음
    else:
        # 죽음의 구간(Forbidden Interval) 세팅
        L_interval = (-delta_L + E_L + 1) % M_mod
        R_interval = (-delta_L - E_L - 1) % M_mod
        Len_L = (R_interval - L_interval) % M_mod
        I_L = (Z0_L - L_interval) % M_mod
        
        if I_L <= Len_L:
            k_L = 0 + N
        else:
            if J == 0:
                k_L = INF
            else:
                k_L = first_hit_in_interval(J, M_mod, M_mod - I_L, M_mod - I_L + Len_L) + N

    # RIGHT 팀의 패배 지점(k_R) 도출
    # 첫 번째 RIGHT 벽 타격 시점의 Y축 거리 계산 (수평 이동 거리는 B - X)
    D0_R = Y * VX + VY * (B - X)
    Z0_R = (2 * D0_R) % M_mod
    
    E_R = W * M * 2 * B
    delta_R = (M * S) % M_mod
    distance_R = min(delta_R, M_mod - delta_R)
    
    if distance_R <= E_R:
        k_R = INF
    else:
        L_interval = (-delta_R + E_R + 1) % M_mod
        R_interval = (-delta_R - E_R - 1) % M_mod
        LEN_R = (R_interval - L_interval) % M_mod
        I_R = (Z0_R - L_interval) % M_mod
        
        if I_R <= LEN_R:
            k_R = 0 + M
        else:
            if J == 0:
                k_R = INF
            else:
                k_R = first_hit_in_interval(J, M_mod, M_mod - I_R, M_mod - I_R + LEN_R) + M
                
    # 먼저 패배하는 팀을 가려내서 최종 정답을 출력합니다.
    # ==가 아닌 >=인 이유는 INF + N 연산으로 인해 커진 값을 방어하기 위함
    if k_L >= INF and k_R >= INF:
        print(f"Case #{number}: DRAW")
    # 공이 우측을 먼저 치므로, 같은 타격 횟수일 경우 RIGHT 팀이 시간상 먼저 실패하게 됨
    elif k_R <= k_L:
        print(f"Case #{number}: {original_L} {k_R}")
    else:
        print(f"Case #{number}: {original_R} {k_L}")