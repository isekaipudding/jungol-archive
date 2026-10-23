# 링크 : https://jungol.co.kr/problem/10821
import sys

input = sys.stdin.readline

# 에디토리얼 : https://icpcarchive.github.io/ICPC-World-Finals/2018-ICPC-World-Finals/solutions/D.html

LIMIT = 1000

fact = [0] * (LIMIT + 1)

# 초기식
fact[0] = 1

# 점화식
for i in range(1, LIMIT + 1, 1):
    fact[i] = i * fact[i - 1]

def coff(n, k):
    if k < 0 or k > n:
        return 0
    return fact[n] // fact[k] // fact[n - k]

N, D, R = map(int, input().split())

# 1. Python의 병목 구간을 피하기 위해 미리 coff 실수값을 구합니다.
C_float = [[0.0] * (N + D + 1) for _ in range(N + D + 1)]
for i in range(N + D + 1):
    for j in range(i + 1):
        C_float[i][j] = float(coff(i, j))
        
# 2. dp[j][i] : j개의 쪼개진 보석을 i명의 사람에게 분배했을 때 상위 R명의 기대 보석 수
dp:list[list[float]] = [[0.0] * (N + 1) for _ in range(D + 1)]

# 3. 초기식 (보석이 단 한 번도 쪼개지지 않은 경우 j = 0)
for i in range(1, N + 1, 1):
    if i <= R:
        # If n ≤ r, S(n, d) = n + d
        dp[0][i] = float(i)
    else:
        dp[0][i] = float(R)
        
# 4. 점화식 (O(N * D * min(N, D)) -> 최대 약 4,100만 번의 루프)
for j in range(1, D + 1, 1):
    lookup = [0.0] * (j + 1)
    for k in range(1, min(N, j) + 1):
        lookup[k] = dp[j - k][k]
        
    c_j_minus_1 = C_float[j - 1]
    
    for i in range(1, N + 1, 1):
        if i <= R:
            # If n ≤ r, S(n, d) = n + d
            dp[j][i] = float(i + j)
        else:
            # (n+d−1)C(d)
            inv_denom = 1.0 / C_float[i + j - 1][j]
            c_i = C_float[i]
            
            # ∑g=0n nCg S(n − g, d − n + g)
            expected_sum = 0.0
            limit = i if i < j else j
            
            for k in range(1, limit + 1, 1):
                # i명 중 k명이 보석을 받고, j개의 보석이 k명에게 분배될 확률 
                expected_sum += c_i[k] * c_j_minus_1[k - 1] * lookup[k]
                
            # S(n, d) = (n+d−1)C(d) ( r + ∑g=0n nCg S(n − g, d − n + g) )
            dp[j][i] = float(R) + expected_sum * inv_denom

result:float = dp[D][N]

print(result)