# 링크 : https://jungol.co.kr/problem/1574
import sys
import math

input = sys.stdin.readline

N:int = int(input().rstrip())

L1:list = [0] * (N + 1)
L2:list = [0] * (N + 1)

for m in range(2, N):
    max_n_limit = (N // (2 * m)) - m
    
    if max_n_limit <= 0:
        break
        
    max_n = min(m - 1, max_n_limit)

    start_n = 1 if m % 2 == 0 else 2

    for n in range(start_n, max_n + 1, 2):
        if math.gcd(m, n) == 1:
            S_p = 2 * m * (m + n)
            L1[S_p] += 1

            for k_S in range(S_p * 2, N + 1, S_p):
                L2[k_S] += 1

result = sum(L1)

result += sum(1 for x, y in zip(L1, L2) if x == 0 and y == 1)

print(result)