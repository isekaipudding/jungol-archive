# 링크 : https://jungol.co.kr/problem/19377
import sys

input = sys.stdin.readline
sys.setrecursionlimit(1 << 21)

# 아 잠만 뭐 이렇게 이해하기 어려워ㄷㄷ

# 에디토리얼 : https://u.acmicpc.net/53941351-d009-489e-a8fe-4654aadaa1ac/ucpc20-finals-solutions.pdf
# xudyh's sieve 참고 자료 1 : https://xy-plane.tistory.com/19
# xudyh's sieve 참고 자료 2 : https://codeforces.com/blog/entry/54150?mobile=true

MOD = 1_000_000_007
LIMIT = 2_000_000

INV2 = pow(2, MOD - 2, MOD)
INV3 = pow(3, MOD - 2, MOD)
INV4 = pow(4, MOD - 2, MOD)

# 1. 선형 체(Linear Sieve)를 이용한 오일러 피 함수 및 누적합 전처리
phi = [0] * LIMIT
phi[1] = 1
primes = []
is_prime = [True] * LIMIT
is_prime[0] = is_prime[1] = False

for i in range(2, LIMIT):
    if is_prime[i]:
        primes.append(i)
        phi[i] = i - 1
    for p in primes:
        if i * p >= LIMIT:
            break
        is_prime[i * p] = False
        if i % p == 0:
            phi[i * p] = phi[i] * p
            break
        else:
            phi[i * p] = phi[i] * (p - 1)

# f0 = phi(n), f1 = n*phi(n), f2 = n^2*phi(n) 의 O(N) 선형 누적합
S0 = [0] * LIMIT
S1 = [0] * LIMIT
S2 = [0] * LIMIT
for i in range(1, LIMIT, 1):
    S0[i] = (S0[i - 1] + phi[i]) % MOD
    S1[i] = (S1[i - 1] + i * phi[i]) % MOD
    S2[i] = (S2[i - 1] + i * i % MOD * phi[i]) % MOD

# 2. Xudyh's Sieve (디리클레 합성곱 기반 O(N^(2/3)) 누적합 가속기)
# 하지만 중복 연산을 방지하기 위해 3개의 누적합을 한 번의 트리 탐색으로 동시 계산
cache = dict()

def calculate_all(x):
    if x <= 0: return (0, 0, 0)
    if x < LIMIT: return (S0[x], S1[x], S2[x])
    if x in cache: return cache[x]
    
    temp0 = temp1 = temp2 = 0
    index = 2
    
    # 이전 구간 끝점(index - 1 = 1)의 g 누적합 초기값
    prev_g0 = prev_g1 = prev_g2 = 1
    
    while index <= x:
        q = x // index
        la = x // q
        
        # la에 대한 g0, g1, g2 누적합을 한 번에 계산
        curr_g0 = la % MOD
        curr_g1 = la * (la + 1) % MOD * INV2 % MOD
        curr_g2 = curr_g1 * (2 * la + 1) % MOD * INV3 % MOD # n(n+1)/2 * (2n+1)/3 = n(n+1)(2n+1)/6

        g_sum0 = (curr_g0 - prev_g0) % MOD
        g_sum1 = (curr_g1 - prev_g1) % MOD
        g_sum2 = (curr_g2 - prev_g2) % MOD

        # 재귀 호출도 단 한 번만 수행하여 재귀 호출에 의한 시간 상수를 크게 낮춥니다.
        sub0, sub1, sub2 = calculate_all(q)

        temp0 = (temp0 + g_sum0 * sub0) % MOD
        temp1 = (temp1 + g_sum1 * sub1) % MOD
        temp2 = (temp2 + g_sum2 * sub2) % MOD

        prev_g0, prev_g1, prev_g2 = curr_g0, curr_g1, curr_g2
        index = la + 1

    # (f * g)(x) 의 누적합: 각각 g1(x), g2(x), g1(x)^2 과 정확히 일치함
    c0 = x * (x + 1) % MOD * INV2 % MOD
    c1 = c0 * (2 * x + 1) % MOD * INV3 % MOD
    c2 = c0 * c0 % MOD

    result = ((c0 - temp0) % MOD, (c1 - temp1) % MOD, (c2 - temp2) % MOD)
    cache[x] = result
    return result

N, M, A, B = map(int, input().split())

limit_d = min(N, M)
complex_sum = 0
i = 1

# 이전 턴의 누적합을 기억하여 호출 횟수 단축
prev_s0 = prev_s1 = prev_s2 = 0

# 3. 에디토리얼 56p: 최후의 3중 시그마 고속 연산 구간
while i <= limit_d:
    u = N // i
    v = M // i
    la = min(N // u, M // v)
    
    curr_s0, curr_s1, curr_s2 = calculate_all(la)
    
    sum_phi = (curr_s0 - prev_s0) % MOD
    sum_dphi = (curr_s1 - prev_s1) % MOD
    sum_d2phi = (curr_s2 - prev_s2) % MOD
    
    prev_s0, prev_s1, prev_s2 = curr_s0, curr_s1, curr_s2
    
    # term_a = phi(d) * (n+1)(m+1) * u * v
    term_a = sum_phi * ((N + 1) * (M + 1) % MOD) % MOD * u % MOD * v % MOD
    
    # term_b = d*phi(d) * ( (n+1)u*v*(v+1) + (m+1)v*u*(u+1) ) / 2
    inner_b = ((N + 1) * (v + 1) + (M + 1) * (u + 1)) % MOD
    term_b = sum_dphi * u % MOD * v % MOD * inner_b % MOD * INV2 % MOD
    
    # term_c = d^2*phi(d) * u(u+1) * v(v+1) / 4
    term_c = sum_d2phi * u % MOD * (u + 1) % MOD * v % MOD * (v + 1) % MOD * INV4 % MOD
    
    # 파이썬은 음수 모듈로를 자동으로 양수 처리하므로 그대로 가감산
    complex_sum = (complex_sum + term_a - term_b + term_c) % MOD
    
    i = la + 1
    
n_term = N * (N + 1) % MOD
m_term = M * (M + 1) % MOD

# 4. 에디토리얼 52p: 최종 다항식 조립 
# result1 = A * n(n+1) * m(m+1)
result1 = A * n_term % MOD * m_term % MOD

# result2 = B * n(n+1) * m(m+1) * (n+m+4) / 3
# 에디토리얼에서는 (n+m+1)으로 되어 있던데 제대로 전개하면 (n+m+4)가 맞아 보입니다.
result2 = B * n_term % MOD * m_term % MOD * (N + M + 4) % MOD * INV3 % MOD

# result3 = 4(A-2B) * complex_sum
result3 = 4 * (A - 2 * B) % MOD * complex_sum % MOD

final_result = (result1 + result2 + result3) % MOD
print(final_result)