# 링크 : https://jungol.co.kr/problem/2797
import sys
import math

input = sys.stdin.readline

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

D1, D2 = map(int, input().split())

total_seats:int = 0

for b in range(1, D2 + 1, 1):
    if D2 // b > (D1 - 1) // b:
        total_seats += phi(b)

print(total_seats)