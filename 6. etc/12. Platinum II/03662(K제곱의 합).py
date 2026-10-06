# 링크 : https://jungol.co.kr/problem/3662
"""
N <= 10^9, K <= 1000  --->  플레티넘 2티어
N <= 10^18, K <= 1000000  --->  다이아 4티어
"""
import sys

input = sys.stdin.readline

# 파울-하버 공식을 적용해서 문제를 해결해봅시다.

MOD = 1_000_000_007

def coff(n, r):
    return FACT[n] * INV_FACT[r] % MOD * INV_FACT[n - r] % MOD

N, K = map(int, input().split())

# 1. 팩토리얼 및 역원 사전 계산
FACT = [1] * (K + 2)
INV_FACT = [1] * (K + 2)

for i in range(1, K + 2):
    FACT[i] = (FACT[i - 1] * i) % MOD
    
INV_FACT[K + 1] = pow(FACT[K + 1], MOD - 2, MOD)
for i in range(K, -1, -1):
    INV_FACT[i] = (INV_FACT[i + 1] * (i + 1)) % MOD

# 2. 베르누이 수(B_m) 동적 계산
B:list = [0] * (K + 1)

# 베르누이 수 초기식
B[0] = 1

# 베르누이 수 점화식 -> B_m = -1/(m+1) * sum(comb(m+1, j) * B_j)
for m in range(1, K + 1):
    s = 0
    for j in range(m):
        s = (s + coff(m + 1, j) * B[j]) % MOD
        
    # 나누기 (m+1) 대신 pow(m+1, MOD - 2, MOD)를 곱함
    B[m] = (-s * pow(m + 1, MOD - 2, MOD)) % MOD

# 3. 파울-하버 공식(Faulhaber's formula) 적용
# S_K(N) = 1/(K+1) * sum_{j=0}^{K} (-1)^j * comb(K+1, j) * B_j * N^{K+1-j}
result:int = 0
for index in range(K + 1):
    # comb(K+1, j) * B_j * N^{K+1-j} 계산
    TEMP = ((coff(K + 1, index) * B[index]) % MOD * pow(N, K + 1 - index, MOD)) % MOD
    
    # (-1)^j 적용 후 (-1)^j * comb(K+1, j) * B_j * N^{K+1-j} 구하고
    # 그 다음 for문에 의해 sigma 값을 구합니다.
    result = (result + TEMP - 2 * (index & 1) * TEMP) % MOD

# 마지막으로 1/(K+1) 곱하기
result = (result * pow(K + 1, MOD - 2, MOD)) % MOD

print(result)