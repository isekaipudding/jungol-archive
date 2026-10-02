# 링크 : https://jungol.co.kr/problem/2813
import sys
import math

input = sys.stdin.readline

def lower_binary_search(array:list, target:int) -> int :
    lo, hi = 0, len(array) - 1
    
    while lo <= hi :
        mid:int = (lo + hi) // 2
        
        if array[mid] == target :
            return mid
        elif array[mid] < target :
            lo = mid + 1
        else :
            hi = mid - 1
            
    return lo

def upper_binary_search(array:list, target:int) -> int :
    lo, hi = 0, len(array) - 1
    
    while lo <= hi :
        mid:int = (lo + hi) // 2
        
        if array[mid] == target :
            return mid
        elif array[mid] < target :
            lo = mid + 1
        else :
            hi = mid - 1
            
    return hi

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

# 최대 10000000까지이므로 10000000 이하의 모든 소수들을 구합니다.
primes:list = eratosthenes_sieve(10000000)

M, N = map(int, input().split())

lo, hi = lower_binary_search(primes, M), upper_binary_search(primes, N)

print(hi + 1 - lo)