# 링크 : https://jungol.co.kr/problem/15877
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

def check(n:int, p:int):
    # 5^4^3^2^1는 p의 최대값을 한참 뛰어넘기 때문에 n이 5 이상이면 무조건 b >= phi(m) 보장
    if n >= 5:
        return True
    # 4^3^2^1 >= phi(m)
    if n == 4 and p <= 262144:
        return True
    # 3^2^1 >= phi(m)
    if n == 3 and p <= 9:
        return True
    # 2^1 >= phi(m)
    if n == 2 and p <= 2:
        return True
    # 1 >= phi(m)
    if n == 1 and p <= 1:
        return True
    return False

def dfs(a:int, m:int):
    if m == 1:
        return 0
    if a == 1:
        return 1
    p:int = phi(m)
    # mod m에 관하여 a^b와 a^{(b mod phi(m)) + phi(m)}은 서로 합동입니다.
    # 이건 b >= phi(m)일 때만 성립하는군요.
    # 만약 b < phi(m)이면 a^b mod m 연산합니다.
    return pow(a, dfs(a-1, p) + p, m) if check(a-1, p) else pow(a, dfs(a-1, p), m)

N, M = map(int, input().split())

result:int = dfs(N, M)
print(result)