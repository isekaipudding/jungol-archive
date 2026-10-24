# 링크 : https://jungol.co.kr/problem/10850
import sys

sys.set_int_max_str_digits(20000)
input = sys.stdin.readline

# 확장 유클리드 호제법
# r1: 최대공약수
# x1, y1: A*x1 + B*y1 = g를 만족하는 계수
def ext_gcd(A:int, B:int):
    r1, r2 = A, B
    x1, x2 = 1, 0
    y1, y2 = 0, 1
    
    while r2:
        q = r1 // r2
        r1, r2 = r2, r1 - q * r2
        x1, x2 = x2, x1 - q * x2
        y1, y2 = y2, y1 - q * y2

    return r1, x1, y1

def check(m: int) -> bool:
    if m == 0:
        return True
    
    pow_10 = 10 ** m
    D_m = d * (pow_10 - 1) // 9
    
    # 1. 확장 유클리드 한 번으로 최대공약수(g)와 x 계수를 동시에 획득
    g, x, y = ext_gcd(pow_10, b)
    
    # 2. 해의 존재 여부 판별
    if D_m % g != 0:
        return False
    
    b_rem = b // g
    
    # 3. 디오판토스 방정식 원리로 k를 구합니다.
    # 기존 방정식: pow_10 * x + b * y = g
    # 양변에 C = (-D_m // g)를 곱하면 원하는 상수항이 됩니다.
    C = -D_m // g
    k = (x * C) % b_rem
    
    X = D_m + k * pow_10
    
    if X == 0:
        X = b_rem * pow_10
    
    return X <= a

def parametric_search():
    low, high = 0, 10000
    best = 0
    
    while low <= high:
        mid = (low + high) // 2
        
        if check(mid):
            best = mid
            low = mid + 1
        else:
            high = mid - 1
    
    return best

b, d, a = map(int, input().split())

print(parametric_search())