# 링크 : https://jungol.co.kr/problem/10258
import sys
import math

input = sys.stdin.readline

# 치환 적분, 오일러-라그랑주 방정식, 룽게-쿠타 방법, 사격 오차 함수, 르장드르 조건 등 온갖 수학 공식이 난무합니다.
# 이게 알고리즘 대회에 나왔다고요? 이거 어떻게 풀어요 진심으로???

# 환경 매개변수 설정
R0 = 1.0    # 자연 방사선량 (uSv / h)
v = 1.0     # 배의 평균 속력 (km / h)
K = 1.0     # 인공 방사선원 강도 (uSv * km^2 / h)
x_A = -10.0 # 출발 지점 x 좌표
x_B = 10.0  # 도착 지점 x 좌표
x_C = 0.0   # 섬의 지점 x 좌표
dx = 0.01  # 1 step 기준의 x 변화량

def get_S_and_T(x, y, y_prime):
    # 개별 섬의 방사선량(P_i)을 한 번만 계산하여 S(x, y)와 T(x, y, y')를 동시에 도출
    S = 0.0
    T = 0.0
    
    for C_ix, C_iy, K_i in islands:
        # 거리 제곱 D_i
        # (섬의 중심을 정확히 관통할 때의 0으로 나누기 에러 방지를 위해 미세값 1e-12 추가)
        D_i = (x - C_ix)**2 + (y - C_iy)**2 + 1e-12 
        
        # 개별 방사선량 P_i
        P_i = K_i / D_i
        
        S += P_i
        T += (P_i / D_i) * (y_prime * (x - C_ix) - (y - C_iy))
        
    return S, T

def get_y_double_prime(x, y, y_prime):
    # 비선형 미분방정식에 x, y, y'를 직접 대입해서 y''를 구합니다.
    S, T = get_S_and_T(x, y, y_prime)
    return 2.0 * (1.0 + y_prime**2) * T / (R0 + S)

def get_total_P(R0, x, y):
    # 특정 위치(x, y)에서의 총 방사선장 P(x, y)
    S, _ = get_S_and_T(x, y, 0.0) # T는 필요 없으므로 y_prime=0.0 전달
    return R0 + S

def rk4_step(x, y, y_prime, dx):
    # k1
    k1_y = y_prime
    k1_yp = get_y_double_prime(x, y, y_prime)
    
    # k2
    k2_y = y_prime + 0.5 * dx * k1_yp
    k2_yp = get_y_double_prime(x + 0.5 * dx, y + 0.5 * dx * k1_y, y_prime + 0.5 * dx * k1_yp)
    
    # k3
    k3_y = y_prime + 0.5 * dx * k2_yp
    k3_yp = get_y_double_prime(x + 0.5 * dx, y + 0.5 * dx * k2_y, y_prime + 0.5 * dx * k2_yp)
    
    # k4
    k4_y = y_prime + dx * k3_yp
    k4_yp = get_y_double_prime(x + dx, y + dx * k3_y, y_prime + dx * k3_yp)
    
    # 다음 Step 계산
    next_y = y + (dx / 6.0) * (k1_y + 2.0*k2_y + 2.0*k3_y + k4_y)
    next_yp = y_prime + (dx / 6.0) * (k1_yp + 2.0*k2_yp + 2.0*k3_yp + k4_yp)
    
    return next_y, next_yp

def simulate_path(x_A, y_A, x_B, initial_slope, dx):
    x = x_A
    y = y_A
    y_prime = initial_slope
    
    while x < x_B:
        step = min(dx, x_B - x)
        if step < 1e-9:
            break
        y, y_prime = rk4_step(x, y, y_prime, step)
        x += step
        
    return y  # 도착점에서의 y 좌표 반환

def find_all_hitting_slopes(x_A, y_A, x_B, y_B, dx):
    slopes:list = [-10.0]  # 최소 한계 기울기
    for C_ix, C_iy, K_i in islands:
        direct_slope = (C_iy - y_A) / (C_ix - x_A)
        slopes.append(direct_slope)
    slopes.append(10.0) # 최대 한계 기울기
    slopes.sort()
    
    valid_initial_slopes = []
    
    for i in range(len(slopes) - 1):
        left = slopes[i]
        right = slopes[i+1]
        
        for _ in range(100):
            mid = (left + right) / 2.0
            final_y = simulate_path(x_A, y_A, x_B, mid, dx)
            
            if final_y > y_B:
                right = mid
            else:
                left = mid
                
        valid_initial_slopes.append((left + right) / 2.0)
    
    valid_initial_slopes.sort()
        
    return valid_initial_slopes

def calculate_total_radiation(x_A, y_A, x_B, R0, v, optimal_slope, dx):
    x = x_A
    y = y_A
    y_prime = optimal_slope
    total_I = 0.0
    
    while x < x_B:
        step = min(dx, x_B - x)
        if step < 1e-9:
            break
            
        # 현재 위치의 피적분 함수값: (P(x,y) / v) * sqrt(1 + y'^2)
        f_current = (get_total_P(R0, x, y) / v) * math.sqrt(1.0 + y_prime**2)
        
        # RK4로 다음 위치 계산
        next_y, next_y_prime = rk4_step(x, y, y_prime, step)
        next_x = x + step
        
        # 다음 위치의 피적분 함수값
        f_next = (get_total_P(R0, next_x, next_y) / v) * math.sqrt(1.0 + next_y_prime**2)
        
        # 사다리꼴 공식(Trapezoidal rule)으로 면적 누적
        total_I += 0.5 * (f_current + f_next) * step
        
        x, y, y_prime = next_x, next_y, next_y_prime
        
    return total_I

T:int = int(input().rstrip())

for number in range(1, T + 1, 1):
    query:list = list(map(str, input().split()))
    N, y_A, y_B = int(query[0]), float(query[1]), float(query[2])
    y_C_list:list = list(map(float, input().split()))
    
    islands:list = [None for _ in range(N)]
    
    for i in range(N):
        C_ix = x_C                   # 섬의 x 좌표
        C_iy = y_C_list[i]           # 섬의 y 좌표
        K_i = K                      # 해당 섬의 인공 방사선원 강도
        islands[i] = (C_ix, C_iy, K) # 섬의 정보 저장
    
    h:float = dx # 1 step 기준의 x 변화량
    
    candidate_slopes:list = find_all_hitting_slopes(x_A, y_A, x_B, y_B, h)

    min_radiation:float = float('inf')
    best_slope:float = 0.0

    for slope in candidate_slopes:
        current_radiation:float = calculate_total_radiation(x_A, y_A, x_B, R0, v, slope, h)
        
        if current_radiation < min_radiation:
            min_radiation = current_radiation
            best_slope = slope
    
    print(f"Case #{number}: {min_radiation:.3f}")