# 링크 : https://jungol.co.kr/problem/13435
import sys
import math
import random
import bisect
from collections import Counter

input = sys.stdin.readline
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

# 소인수 리스트를 받아 p의 모든 약수를 오름차순 정렬된 리스트로 반환합니다.
def get_all_divisors(prime_factors):
    factor_counts = Counter(prime_factors)
    divisors = [1]
    
    for prime, count in factor_counts.items():
        new_divisors = []
        multiplier = 1
        for _ in range(count + 1):
            for d in divisors:
                new_divisors.append(d * multiplier)
            multiplier *= prime
        divisors = new_divisors
        
    divisors.sort()
    return divisors

while True:
    p:int = int(input().rstrip())

    if p == 0:
        break
        
    # 1. 예외 처리: 부피가 1인 경우
    if p == 1:
        print(3)
        continue
        
    # 2. 폴라드 로 알고리즘으로 소인수 분해
    factors = []
    factorize(p, factors)
    
    # 3. 분해된 소인수들로 모든 약수 생성 및 정렬
    divisors = get_all_divisors(factors)
    
    result = float('inf')
    
    # 4. w의 탐색 한계 설정(세제곱근)
    # 부동소수점 오차를 방지하기 위해 넉넉하게 +2를 해줍니다. 
    # (어차피 bisect가 실제 존재하는 약수로 정확히 잡아줍니다.)
    limit_w = int(p ** (1/3)) + 2
    
    # 원래라면 w 찾는데 O(p), d 찾는데 O(p)이 걸려 O(p^2)이 걸리나
    # "어차피 w, d, h는 최소값을 가질려면 p^(1/3) 근처에 있어야 한다"는 그리디 해법이 생각나서
    # 이진 탐색으로 p^(1/3) 근처부터 시작합니다.
    # 시간 복잡도는 O(p^2) -> O(p^(1/3) log p)로 최적화 됩니다.
    # 심지어 그냥 p도 아닌 d(p) 수준으로 탐색 범위를 확 좁혀 실제 걸리는 시간은 엄청 짧습니다.
    
    # 첫 번째 이진 탐색 (w 시작점 찾기)
    start_w_index = bisect.bisect_right(divisors, limit_w) - 1
    
    # w를 세제곱근 근처부터 "역순"으로 탐색
    for i in range(start_w_index, -1, -1):
        w = divisors[i]
        temp = p // w
        
        # 5. d의 탐색 한계 설정 (남은 값의 제곱근)
        # math.isqrt를 사용하면 부동소수점 오차 없이 정확한 정수 제곱근을 반환합니다.
        limit_d = math.isqrt(temp)
        
        # 두 번째 이진 탐색 (d 시작점 찾기)
        start_d_index = bisect.bisect_right(divisors, limit_d) - 1
        
        # d를 제곱근 근처부터 "역순"으로 탐색
        for j in range(start_d_index, -1, -1):
            d = divisors[j]
            
            # 정수로 나누어 떨어지는(약수인) d를 찾은 순간
            if temp % d == 0:
                h = temp // d
                current_sum = w + d + h
                
                if current_sum < result:
                    result = current_sum
                    
                # [Greedy Break]
                # 역순 탐색 중 최초로 발견된 (d, h) 쌍은 무조건 두 수의 격차가 가장 작은 쌍입니다.
                # 산술-기하 평균 부등식에 의해 이 합이 현재 w에서 만들 수 있는 절대적 최소합이므로
                # 더 작은 d를 찾기 위해 내부 루프를 돌 필요가 전혀 없습니다! 즉시 탈출합니다.
                break 
                
    print(result)