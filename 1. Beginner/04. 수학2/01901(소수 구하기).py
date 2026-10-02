# 링크 : https://jungol.co.kr/problem/1901
import sys
import math

input = sys.stdin.readline

def binary_search(array:list, target:int) -> list :
    lo, hi = 0, len(array) - 1
    
    while lo <= hi :
        mid:int = (lo + hi) // 2
        
        if array[mid] == target :
            return [mid]
        elif array[mid] < target :
            lo = mid + 1
        else :
            hi = mid - 1
            
    return [hi, lo]

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

# M_i = 1000000인 경우 1000003이 더 가까운 반례를 고려합니다.
primes:list = eratosthenes_sieve(1000003)

N:int = int(input().rstrip())

for _ in range(N) :
    M:int = int(input().rstrip())
    # 예외 처리
    if M == 1 :
        print(2)
        continue
    L:list = binary_search(primes, M)
    
    if len(L) == 1 :
        print(primes[L[0]])
    elif len(L) == 2 :
        A, B = primes[L[0]], primes[L[1]]
        # 만약 M이 A와 B 딱 중간점인 경우 A, B 모두 출력
        if M - A == B - M :
            print(A, B)
        # 만약 M이 B에 더 가깝다면 B 출력
        elif M - A > B - M :
            print(B)
        # 만약 M이 A에 더 가깝다면 A 출력
        else :
            print(A)