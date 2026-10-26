# 링크 : https://jungol.co.kr/problem/1163
import sys
import math

input = sys.stdin.readline

# 백준 링크 : https://www.acmicpc.net/problem/1016

def eratosthenes_sieve(n:int) -> list :
    if n < 2 :
        return []
    
    is_prime:list = [True] * (n + 1)
    
    is_prime[0], is_prime[1] = False, False
    
    for i in range(4, n + 1, 2) :
        is_prime[i] = False
        
    for i in range(3, int(math.sqrt(n)) + 1, 2) :
        if is_prime[i] :
            for j in range(i * i, n + 1, 2 * i) :
                is_prime[j] = False
                
    return [index for index, value in enumerate(is_prime) if value]

A, B = map(int, input().split())

# 런타임 전처리 과정: B의 제곱근까지만 소수를 구하면 충분함
primes:list = eratosthenes_sieve(math.isqrt(B))

# B - A는 최대 1,000,000이므로 1,000,001 크기의 배열 생성
size:int = B - A + 1
is_square_free:list = [True] * size

# 구한 소수들을 순회하며 구간 내의 제곱인수 배수들을 걸러냄
for prime in primes:
    p_square:int = prime * prime
    
    # A 이상의 수 중에서 p_square로 나누어 떨어지는 가장 작은 수(start) 계산
    start:int = (A // p_square) * p_square
    if start < A:
        start += p_square
        
    # start값의 실제 리스트 인덱스
    start_index:int = start - A
    
    # 해당 소수의 제곱수의 배수들을 모두 False로 변경
    for j in range(start_index, size, p_square):
        is_square_free[j] = False

# True로 살아남은(제곱수로 나누어 떨어지지 않는) 원소들의 개수 합산
result:int = sum(is_square_free)
print(result)