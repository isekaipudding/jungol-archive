# 링크 : https://jungol.co.kr/problem/1166
import sys
import math

input = sys.stdin.readline

def is_prime(N:int) -> bool :
    if N < 2:
        return False
    if N == 2 or N == 3:
        return True  # 2와 3은 소수
    if N % 2 == 0 or N % 3 == 0:
        return False # 2나 3의 배수는 모두 제외

    # 5부터 시작해서 6씩 건너뜁니다. (i는 6k-1, i+2는 6k+1에 대응)
    i:int = 5
    while i * i <= N :
        if N % i == 0 or N % (i + 2) == 0:
            return False
        i += 6
        
    return True

def phi(N:int) :
    result:int = N
    for p in range(2, int(math.sqrt(N))+1, 1) :
        if N % p == 0 :
            # n * (1 - 1/p) = N - N / p
            result -= result // p
            while N % p == 0 :
                N //= p
                
    # 만약 N > 1이면 그 N은 소수이므로 N - N / p 계산하기
    if N > 1 :
        result -= result // N
    
    return result

while True :
    N:int = int(input().rstrip())
    if N == 0 :
        break
    
    # 예외 처리 1
    if N == 1 :
        print(1)
        continue
    
    # 예외 처리 2
    # 오일러 피 함수에서 N이 소수이면 N * {(N-1)/N} = N-1이 됩니다.
    if is_prime(N) :
        print(N - 1)
        continue
    
    print(phi(N))