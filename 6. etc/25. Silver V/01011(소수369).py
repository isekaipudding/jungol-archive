# 링크 : https://jungol.co.kr/problem/1011
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

N, M, K = map(int, input().split())

primes:list = eratosthenes_sieve(M)

# 0-based index -> 1-based index
K += 1

result:int = 0

for p in primes :
    if (p - K) % N == 0 :
        result += 1

print(result)