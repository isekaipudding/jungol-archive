# 링크 : https://jungol.co.kr/problem/3662
"""
N <= 10^9, K <= 1000  --->  플레티넘 2티어
N <= 10^18, K <= 1000000  --->  다이아 4티어
"""
import sys

input = sys.stdin.readline

# 라그랑주 보간법을 적용해서 문제를 해결해봅시다.

MOD = 1_000_000_007

N, K = map(int, input().split())

# 0. Base Case(N이 K+1 이하라면 보간법 없이 직접 구해버리는 게 빠름)
# K 이게 최대 10^6이라면 베르누이 수 구하는 과정에서 TLE가 발생하므로
# 차라리 무식한 브루트 포스 방식이 오히려 더 낫습니다.
if N <= K + 1:
    result = 0
    for i in range(1, N + 1):
        result = (result + pow(i, K, MOD)) % MOD
    print(result)
    sys.exit(0)

# 1. y 좌표값 계산 -> y[i] = f(i) = sum(j^K)
y = [0] * (K + 2)
for i in range(1, K + 2):
    # i^K를 O(log K)만에 계산하여 누적
    y[i] = (y[i - 1] + pow(i, K, MOD)) % MOD

# 2. 분모를 위한 팩토리얼 역원 계산
FACT = [1] * (K + 2)
INV_FACT = [1] * (K + 2)

for i in range(1, K + 2):
    FACT[i] = (FACT[i - 1] * i) % MOD
    
INV_FACT[K + 1] = pow(FACT[K + 1], MOD - 2, MOD)
for i in range(K, -1, -1):
    INV_FACT[i] = (INV_FACT[i + 1] * (i + 1)) % MOD

# 3. 분자를 위한 누적 곱(Prefix & Suffix Array)
# prefix[i] = (N) * (N-1) * ... * (N-i)
prefix = [1] * (K + 2)
prefix[0] = N % MOD
for i in range(1, K + 2):
    prefix[i] = (prefix[i - 1] * ((N - i) % MOD)) % MOD

# suffix[i] = (N-i) * (N-i-1) * ... * (N-(K+1))
suffix = [1] * (K + 2)
suffix[K + 1] = (N - (K + 1)) % MOD
for i in range(K, -1, -1):
    suffix[i] = (suffix[i + 1] * ((N - i) % MOD)) % MOD

# 4. 라그랑주 보간법(Lagrange Interpolation) 적용
result:int = 0
for i in range(K + 2):
    # 분자 계산(i번째 항을 뺀 앞뒤의 곱)
    num = 1
    if i > 0:
        num = (num * prefix[i - 1]) % MOD
    if i < K + 1:
        num = (num * suffix[i + 1]) % MOD
        
    # 분모 계산 역원 적용  ->  1 / (i! * (K+1-i)!)
    den_inv = (INV_FACT[i] * INV_FACT[K + 1 - i]) % MOD
    
    # 항 계산
    TEMP = ((y[i] * num) % MOD * den_inv) % MOD
    
    # 분모의 음수 팩토리얼에서 튀어나오는 (-1)^(K+1-i) 부호 결정
    is_odd = (K + 1 - i) & 1
    result = (result + TEMP - 2 * is_odd * TEMP) % MOD

print(result)