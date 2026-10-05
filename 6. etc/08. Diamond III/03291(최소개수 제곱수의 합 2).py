# 링크 : https://jungol.co.kr/problem/3291
"""
관리자에 의해 정해진 티어 : 골드 5티어
실제 난이도 : 플레티넘 4티어(N = 10^10) 기준, 다이아 3티어(N = 10^18 기준)
여기서는 다이아 3티어 폴더에 저장합니다.
"""
import sys
import math
import random
from collections import Counter

input = sys.stdin.readline
# 폴라드 로의 재귀 깊이를 고려하여 제한 해제
sys.setrecursionlimit(1 << 20)

# 라그랑주의 네 제곱수 정리 : https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem
# 르장드르의 세 제곱수 정리 : https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem
# 페르마의 두 제곱수 정리 : https://en.wikipedia.org/wiki/Fermat%27s_theorem_on_sums_of_two_squares

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

def lagrange(N) :
    # 완전 거듭제곱인 경우 어떠한 법칙 적용하지 않고 바로 1개의 제곱수로 표현 가능
    if math.isqrt(N) ** 2 == N :
        return 1
    
    TEMP:int = N
    while TEMP % 4 == 0:
        TEMP >>= 2
    # 르장드르의 세 제곱수 정리에 의해 4^a(8b + 7)가 아닌 경우는 3개 이하의 제곱수의 합으로 가능합니다.
    # 그러나 만약 4^a(8b + 7)이면 제곱수 3개 이하가 불가능하므로 라그랑주의 네 제곱수 정리에 의해 4개입니다.
    if TEMP % 8 == 7 :
        return 4
    
    # 새로 만든 재귀 함수를 호출하여 N을 완벽한 소인수들로 분해합니다.
    factor:list = []
    factorize(N, factor)
            
    # 각 (4k+3) 소수별 지수를 세어, 한 번이라도 홀수인 소수가 있으면 2제곱수로 못 씁니다.
    # 이것을 무시한 경우 N = 21에서 반례가 발생합니다. 그러므로 아래 소스 코드로 합니다.
    for p, exp in Counter(factor).items() :
        if p % 4 == 3 and exp % 2 == 1 :
            return 3
    return 2

T:int = int(input().rstrip())

for _ in range(T):
    N:int = int(input().rstrip())
    print(lagrange(N))