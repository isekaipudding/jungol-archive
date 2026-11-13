# 링크 : https://jungol.co.kr/problem/19397
import sys

input = sys.stdin.readline

# 에디토리얼 : https://static.ucpc.me/files/2021/ucpc21-finals-solutions.pdf

LIMIT = 200000

# NTT 설정
MOD = 998244353
PRIM_ROOT = 3

def modpow(a, e=MOD-2):
    r = 1
    while e:
        if e & 1:
            r = r * a % MOD
        a = a * a % MOD
        e >>= 1
    return r

def ntt(a, invert):
    n = len(a)
    # 비트 반전 순서
    rev = [0] * n
    for i in range(n):
        rev[i] = (rev[i>>1] >> 1) | ((i & 1) * (n >> 1))
    for i in range(n):
        if i < rev[i]:
            a[i], a[rev[i]] = a[rev[i]], a[i]
    # Cooley–Tuk 알고리즘
    length = 1
    while length < n:
        # primitive n-th root 계산
        wlen = modpow(PRIM_ROOT, (MOD - 1) // (length * 2))
        if invert:
            wlen = modpow(wlen)
        for i in range(0, n, length * 2):
            w = 1
            for j in range(length):
                u = a[i + j]
                v = a[i + j + length] * w % MOD
                a[i + j] = (u + v) % MOD
                a[i + j + length] = (u - v + MOD) % MOD
                w = w * wlen % MOD
        length <<= 1
    if invert:
        inv_n = modpow(n)
        for i in range(n):
            a[i] = a[i] * inv_n % MOD

def multiply(A, B):
    need = len(A) + len(B) - 1
    n = 1
    while n < need:
        n <<= 1
    fa = A + [0] * (n - len(A))
    fb = B + [0] * (n - len(B))
    ntt(fa, False)
    ntt(fb, False)
    for i in range(n):
        fa[i] = fa[i] * fb[i] % MOD
    ntt(fa, True)
    return fa[:need]

def calculate_color(target_color, surround_color):
    # T가 바로 누적합 리스트입니다.
    # 에디토리얼 108p 혹은 109p에 있는 Tr - Tl을 O(1) 계산하기 위해 꼭 필요합니다.
    T = [0] * N
    current:int = 0
    
    # 누적합
    for j in range(N):
        if S[j] == target_color:
            current = (current + L[j]) % MOD
        T[j] = current
    
    # 에디토리얼 110p 통해 A와 B 다항식 세팅합니다.
    A = [0] * N
    B = [0] * N
    
    for j in range(N):
        if S[j] == surround_color:
            A[j] = T[j]
            B[(N - 1) - j] = 1
    
    # 에디토리얼 110p에서 A와 B를 FFT 연산하여 C를 구할 수 있습니다.
    C = multiply(A, B)
    
    result = 0
    fact_N_2 = fact[N] * 2 % MOD
    
    # i는 r - l을 의미하며 최소 간격은 2
    # 그 이유는 돌이 1개 이상 사이에 존재해야 하죠.
    for i in range(2, N, 1):
        # g(i) = C_{N+1-1} - C_{N-i-1} (에디토리얼 110p, 1-based index -> 0-based index)
        g_i = (C[(N - 1) + i] - C[(N - 1) - i]) % MOD
        
        # f_i = 2 * N! / ((i+1) * i * (i-1)) (에디토리얼 107p)
        inv_term = inv[i + 1] * inv[i] % MOD * inv[i - 1] % MOD
        f_i = fact_N_2 * inv_term % MOD
        
        # 에디토리얼 108p에서 g_i * f_i 시그마 연산을 진행합니다.
        result = (result + g_i * f_i) % MOD
    
    return result

# 팩토리얼 및 역원 초기화
fact:list = [0] * (LIMIT + 1)
inv:list = [0] * (LIMIT + 1)

# 초기식
fact[0] = 1
inv[1] = 1

# 점화식
for i in range(2, LIMIT + 1, 1):
    inv[i] = (-(MOD // i) * inv[MOD % i]) % MOD
for i in range(1, LIMIT + 1, 1):
    fact[i] = i * fact[i - 1] % MOD

N:int = int(input().rstrip())
S:str = input().rstrip()
L:list = list(map(int, input().split()))

black:int = calculate_color('B', 'W') # 검은색 돌을 가져갈 때
white:int = calculate_color('W', 'B') # 하얀색 돌을 가져갈 때

total_score:int = black + white

print(total_score % MOD)