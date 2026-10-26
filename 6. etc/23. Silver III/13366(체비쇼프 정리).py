# 링크 : https://jungol.co.kr/problem/13366
import sys
import math

input = sys.stdin.readline

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

def parametric_search_max(array:list, target:int) -> bool :
    lo, hi = 0, len(array) - 1
    
    result:int = -1
    
    while lo <= hi :
        mid:int = (lo + hi) // 2
        
        if array[mid] <= target :
            result = mid
            lo = mid + 1
        else:
            hi = mid - 1
            
    return result

def parametric_search_min(array:list, target:int) -> bool :
    lo, hi = 0, len(array) - 1
    
    result:int = -1
    
    while lo <= hi :
        mid:int = (lo + hi) // 2
        
        if array[mid] > target :
            result = mid
            hi = mid - 1
        else:
            lo = mid + 1
            
    return result

primes:list = eratosthenes_sieve(2 * 123456)

while True:
    N:int = int(input().rstrip())
    if N == 0:
        break
    result:int = parametric_search_max(primes, 2 * N) - parametric_search_min(primes, N) + 1
    print(result)