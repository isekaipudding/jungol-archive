# 링크 : https://jungol.co.kr/problem/10101
import sys
import math
import random
from collections import Counter

input = sys.stdin.readline
gcd = math.gcd
# 폴라드 로의 재귀 깊이를 고려하여 제한 해제
sys.setrecursionlimit(1 << 20)

# 단일 base 'a'에 대해 밀러-라빈 소수 판별을 수행합니다.
def miller_rabin(n, a):
    d = n - 1
    while d % 2 == 0:
        d //= 2
    
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True
    
    # d를 2배씩 늘려가며 n-1이 되는지 확인
    while d < n - 1:
        x = pow(x, 2, n)
        if x == n - 1:
            return True
        d *= 2
        
    return False

# N < 2^64 범위에서 100% 정확도를 보장하는 결정론적 소수 판별 함수
def is_prime(n):
    if n <= 1:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # 2^64 이하의 수에 대해 100% 정확도를 보장하는 12개의 소수 Base
    bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for a in bases:
        if n == a:
            return True
        if not miller_rabin(n, a):
            return False
            
    return True

# 폴라드 로 알고리즘을 사용하여 합성수 n의 자명하지 않은 약수 중 하나를 반환합니다.
def pollard_rho(n):
    if is_prime(n):
        return n
    if n % 2 == 0:
        return 2
    
    # 사이클을 찾기 위한 무작위 초기값 설정
    x = random.randrange(2, n)
    y = x
    c = random.randrange(1, n)
    d = 1
    
    while d == 1:
        # 플로이드의 토끼와 거북이(Cycle Detection) 알고리즘
        x = (pow(x, 2, n) + c) % n
        y = (pow(y, 2, n) + c) % n
        y = (pow(y, 2, n) + c) % n
        
        d = math.gcd(abs(x - y), n)
        
        # d == n이면 실패한 경우이므로 무작위 값을 재설정하여 다시 시도
        if d == n:
            x = random.randrange(2, n)
            y = x
            c = random.randrange(1, n)
            d = 1
            
    return d

# 폴라드 로 알고리즘을 재귀적으로 호출하여 소인수분해를 수행합니다.
def factorize(n, factors):
    if n == 1:
        return
    # 소수라면 분해를 멈추고 리스트에 추가
    if is_prime(n):
        factors.append(n)
        return
    
    # 합성수라면 폴라드 로를 이용해 쪼갬
    divisor = pollard_rho(n)
    
    # 쪼개진 두 수에 대해 다시 재귀적으로 소인수분해
    factorize(divisor, factors)
    factorize(n // divisor, factors)

# 소인수 리스트를 바탕으로 모든 약수를 생성하는 함수
def get_all_divisors(n):
    if n == 1:
        return [1]
    
    factors = []
    factorize(n, factors)
    counts:Counter = Counter(factors)
    
    divisors = [1]
    
    for p, count in counts.items():
        new_divisors = []
        power = 1
        for _ in range(count + 1):
            for d in divisors:
                new_divisors.append(d * power)
            power *= p
        divisors = new_divisors
        
    return divisors

# 최소공배수를 구하는 함수
def lcm(a, b):
    return a // gcd(a, b) * b

T:int = int(input().rstrip())

for number in range(1, T + 1, 1):
    N, L, H = map(int, input().split())
    F:list = list(map(int, input().split()))
    F.sort()
    
    prefix_lcm = [0] * N
    current_lcm = F[0]
    prefix_lcm[0] = min(current_lcm, H + 1)
    
    for i in range(1, N, 1):
        current_lcm = lcm(current_lcm, F[i])
        prefix_lcm[i] = min(current_lcm, H + 1)
    
    suffix_gcd = [0] * N
    current_gcd = F[-1]
    suffix_gcd[-1] = current_gcd
    
    for i in range(N - 2, -1, -1):
        current_gcd = gcd(current_gcd, F[i])
        suffix_gcd[i] = current_gcd
    
    result = float('inf')

    for k in range(N + 1):
        
        # 케이스 A: 모든 연주자의 주파수가 X의 배수인 경우 (k=0)
        if k == 0:
            L_k = 1
            G_k = suffix_gcd[0]
            
        # 케이스 B: 모든 연주자의 주파수가 X의 약수인 경우 (k=N)
        elif k == N:
            L_k = prefix_lcm[N - 1]
            G_k = 0 # 0은 모든 수의 배수이므로 상한 제약이 없음을 의미
            
        # 케이스 C: 중간에서 분할되는 일반적인 경우
        else:
            L_k = prefix_lcm[k - 1]
            G_k = suffix_gcd[k]
            
        # 조건 검사 및 X 후보 추출
        if k == N:
            if L_k <= H:
                # L_k의 배수 중 L 이상인 가장 작은 값을 찾음
                min_multiplier = max(1, (L + L_k - 1) // L_k)
                candidate_X = L_k * min_multiplier
                if candidate_X <= H:
                    result = min(result, candidate_X)
                    
        else:
            # L_k가 G_k의 약수일 때만 해가 존재할 수 있음
            if G_k % L_k == 0:
                M = G_k // L_k
                
                # 폴라드 로를 이용해 M의 모든 약수를 순식간에 구함
                divisors = get_all_divisors(M)
                
                for d in divisors:
                    candidate_X = L_k * d
                    if L <= candidate_X <= H:
                        result = min(result, candidate_X)

    if result != float('inf'):
        print(f"Case #{number}: {result}")
    else:
        print(f"Case #{number}: NO")