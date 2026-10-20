# 링크 : https://jungol.co.kr/problem/19849
import sys

read = sys.stdin.read
write = sys.stdout.write

# 이 문제는 C++로 하면 dp를 통해 O(N * M^2)으로 풀 수 있는데 Python으로 하면 TLE가 발생합니다.
# 그러므로 Python으로 통과할려면 대략 O(M log M log N) "키타마사법 + NTT"가 강요됩니다.
# 이렇게 해야 Python으로 통과되더라고요.

# 수론적 변환(NTT, Number Theoretic Transform), Cooley-Tukey 알고리즘
# 참고 자료(이론): https://cp-algorithms.com/algebra/fft.html (CP-Algorithms 공식 FFT/NTT)
# 참고 자료(구현): https://justicehui.github.io/hard-algorithm/2019/09/04/FFT/ (국내 최고 레퍼런스)
# NTT 설정
mod = 998244353
prim_root = 3

def modpow(a, e=mod-2):
    r = 1
    while e:
        if e & 1:
            r = r * a % mod
        a = a * a % mod
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
        wlen = modpow(prim_root, (mod - 1) // (length * 2))
        if invert:
            wlen = modpow(wlen)
        for i in range(0, n, length * 2):
            w = 1
            for j in range(length):
                u = a[i + j]
                v = a[i + j + length] * w % mod
                a[i + j] = (u + v) % mod
                a[i + j + length] = (u - v + mod) % mod
                w = w * wlen % mod
        length <<= 1
    if invert:
        inv_n = modpow(n)
        for i in range(n):
            a[i] = a[i] * inv_n % mod

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
        fa[i] = fa[i] * fb[i] % mod
    ntt(fa, True)
    return fa[:need]


# K x K 행렬 곱셈(희소 행렬 및 캐시 최적화 포함)
def matrix_multiply(A:list[list[int]], B:list[list[int]], size:int, M_MOD:int) -> list[list[int]]:
    result = [[0] * size for _ in range(size)]
    for r in range(size):
        A_r = A[r]
        result_r = result[r]
        for k in range(size):
            a_rk = A_r[k]
            if a_rk == 0:
                continue
            B_k = B[k]
            for c in range(size):
                result_r[c] = (result_r[c] + a_rk * B_k[c]) % M_MOD
    return result

# 행렬의 특성다항식(Characteristic Polynomial), 유클리드 상헤센베르크(Upper Hessenberg) 변환
# 참고 자료(이론): https://en.wikipedia.org/wiki/Hessenberg_matrix
# 나눗셈 없는 유클리드 상헤센베르크 변환 기반 특성다항식 추출: O(K^3)
# 반환값: P(x) = det(xI - A) = c_0 + c_1*x + ... + c_{K-1}*x^{K-1} + 1*x^K
def get_char_poly(A:list[list[int]], size:int, M_MOD:int) -> list[int]:
    H = [row[:] for row in A]
    for j in range(size - 2):
        for i in range(size - 1, j + 1, -1):
            while H[i][j] != 0:
                q = H[i - 1][j] // H[i][j]
                if q != 0:
                    for c in range(j, size):
                        H[i - 1][c] = (H[i - 1][c] - q * H[i][c]) % M_MOD
                    for r in range(size):
                        H[r][i] = (H[r][i] + q * H[r][i - 1]) % M_MOD
                H[i - 1], H[i] = H[i], H[i - 1]
                for r in range(size):
                    H[r][i - 1], H[r][i] = H[r][i], H[r][i - 1]

    polys = [[1]]
    for k in range(1, size + 1):
        prev = polys[k - 1]
        diag = H[k - 1][k - 1]
        current = [0] * (k + 1)
        for deg in range(k):
            current[deg + 1] = prev[deg]
            current[deg] = (current[deg] - diag * prev[deg]) % M_MOD

        prod = 1
        for i in range(k - 2, -1, -1):
            prod = (prod * H[i + 1][i]) % M_MOD
            factor = (H[i][k - 1] * prod) % M_MOD
            if factor != 0:
                p_i = polys[i]
                for deg in range(i + 1):
                    current[deg] = (current[deg] - factor * p_i[deg]) % M_MOD
        polys.append(current)

    return polys[size]

# NTT를 활용한 다항식 곱셈 및 특성다항식 모듈러 축소: (P * Q) mod char_poly
def poly_mul_mod(P:list[int], Q:list[int], char_poly:list[int], size:int, M_MOD:int) -> list[int]:
    if M_MOD == mod or size * (M_MOD - 1) * (M_MOD - 1) < mod:
        raw = multiply(P, Q)
        prod_poly = [x % M_MOD for x in raw]
    else:
        # M_MOD가 임의의 수이고 합성곱 중간값이 998244353을 넘을 때의 안전 분할
        BASE = int(M_MOD ** 0.5) + 1
        P_lo = [x % BASE for x in P]
        P_hi = [x // BASE for x in P]
        raw_lo = multiply(P_lo, Q)
        raw_hi = multiply(P_hi, Q)
        prod_poly = [(lo + hi * BASE) % M_MOD for lo, hi in zip(raw_lo, raw_hi)]

    # 차수 축소: x^size = -(c_0 + c_1*x + ... + c_{size-1}*x^{size-1})
    for deg in range(len(prod_poly) - 1, size - 1, -1):
        coeff = prod_poly[deg]
        if coeff != 0:
            for j in range(size):
                prod_poly[deg - size + j] = (prod_poly[deg - size + j] - coeff * char_poly[j]) % M_MOD

    return prod_poly[:size]

# 키타마사법(Kitamasa Method), 케일리-해밀턴 정리(Cayley-Hamilton Theorem), 다항식 나눗셈
# 참고 자료(이론): https://jiuge-meogari-ps.tistory.com/66 (훌륭한 키타마사 해설 블로그)
# 참고 자료(구현): https://justicehui.github.io/hard-algorithm/2021/03/13/kitamasa/ (국내 키타마사 원탑 블로그)
# 키타마사 본체: x^exponent mod char_poly(x) = r_0 + r_1*x + ... + r_{K-1}*x^{K-1} 반환
def kitamasa(char_poly:list[int], exponent:int, size:int, M_MOD:int) -> list[int]:
    result_poly = [0] * size
    result_poly[0] = 1 % M_MOD

    if exponent == 0:
        return result_poly

    base_poly = [0] * size
    if size > 1:
        base_poly[1] = 1 % M_MOD
    else:
        base_poly[0] = (-char_poly[0]) % M_MOD

    while exponent > 0:
        if exponent & 1:
            result_poly = poly_mul_mod(result_poly, base_poly, char_poly, size, M_MOD)
        exponent >>= 1
        if exponent > 0:
            base_poly = poly_mul_mod(base_poly, base_poly, char_poly, size, M_MOD)

    return result_poly

# 뉴턴 항등식(Newton's Identities), 행렬 대각합(Trace)의 선형성
# 참고 자료(이론): https://en.wikipedia.org/wiki/Newton%27s_identities
# 키타마사법 + 뉴턴 항등식으로 대각합 Tr(A^exponent) 구하기(행렬 곱셈 불필요)
def trace_power_kitamasa(A:list[list[int]], exponent:int, size:int, M_MOD:int) -> int:
    char_poly = get_char_poly(A, size, M_MOD)

    traces = [0] * size
    traces[0] = size % M_MOD
    for k in range(1, size):
        s = (k * char_poly[size - k]) % M_MOD
        for j in range(1, k):
            s = (s + char_poly[size - j] * traces[k - j]) % M_MOD
        traces[k] = (-s) % M_MOD

    if exponent < size:
        return traces[exponent]

    coeffs = kitamasa(char_poly, exponent, size, M_MOD)
    trace_An = 0
    for k in range(size):
        trace_An = (trace_An + coeffs[k] * traces[k]) % M_MOD
    return trace_An

tokens = read().split()
index = 0
num_tokens = len(tokens)
out = []

while index < num_tokens:
    m = int(tokens[index])
    index += 1
    if m == 0:
        break

    f = [int(tokens[index + i]) for i in range(m + 1)]
    index += m + 1

    n = int(tokens[index])
    M_MOD = int(tokens[index + 1])
    index += 2

    # 1. Infinity 판정
    is_inf = False
    for i in range(m):
        current = i
        sign = 1
        for step in range(1, m + 1):
            diff = f[current + 1] - f[current]
            if diff == 1:
                current = f[current]
            elif diff == -1:
                current = f[current + 1]
                sign = -sign
            else:
                current = -1
                break

            if current == i:
                if n % step == 0:
                    if sign == 1 or ((n // step) & 1) == 0:
                        is_inf = True
                break
        if is_inf:
            break

    if is_inf:
        out.append("Infinity\n")
        continue

    # 2. 정수 격자점 주기점 개수 |S_int| 계산
    s_int = 0
    for k in range(m + 1):
        current = k
        for step in range(1, m + 2):
            current = f[current]
            if current == k:
                if n % step == 0:
                    s_int += 1
                break

    # 3. 유향 근방 상태 C_boundary 계산
    next_b = [-1] * (2 * m)
    for k in range(m):
        y0, y1 = f[k], f[k + 1]
        if y0 < y1:
            next_b[k] = y0
            next_b[m + k] = m + (y1 - 1)
        elif y0 > y1:
            next_b[k] = m + (y0 - 1)
            next_b[m + k] = y1

    c_boundary = 0
    for b in range(2 * m):
        current = b
        for step in range(1, 2 * m + 1):
            current = next_b[current]
            if current == -1:
                break
            if current == b:
                if n % step == 0:
                    c_boundary += 1
                break

    # 4. 마르코프 전이 행렬 A 구성
    A = [[0] * m for _ in range(m)]
    for i in range(m):
        low = min(f[i], f[i + 1])
        high = max(f[i], f[i + 1])
        value = 1 % M_MOD
        for j in range(low, high):
            A[i][j] = value

    # 5. 템플릿 함수 호출 한 줄로 Tr(A^n) 계산 완료
    trace_An = trace_power_kitamasa(A, n, m, M_MOD)

    # 6. 경계 보정 후 최종 답안 기록
    result = (trace_An - c_boundary + s_int) % M_MOD
    out.append(f"{result}\n")

write("".join(out))



"""
이 문제는 키타마사법으로 대각합을 O(K^2 log N) 수준으로 최적화한 문제입니다.

그리고 이걸 바탕으로 키타마사법으로 피보나치 수열 dp[N] % MOD를 O(K log N log K)로 구할려면 다음과 같은 소스 코드면 됩니다.
단, 그 이전에 NTT, get_char_poly, kitamasa가 구현되어 있어야 합니다.

import sys

N = 1000000000
MOD = 1000000007
K = 2 # 피보나치 수열은 직전 2개의 항을 참조하므로 K = 2

# N이 0 또는 1일 때는 초기값을 바로 반환
if N == 0:
    print(0)
    sys.exit(0)
elif N == 1:
    print(1)
    sys.exit(0)

# 1. 특성다항식(char_poly) 수동 추출 (O(1))
# 피보나치 점화식: F_N = F_{N-1} + F_{N-2}
# 이항하여 정리: F_N - F_{N-1} - F_{N-2} = 0
# 특성방정식: x^2 - x - 1 = 0
# 템플릿의 char_poly 구조는 [c_0, c_1] 이며 최고차항(x^2) 앞의 계수는 1로 고정
# 즉, P(x) = c_0 + c_1*x + 1*x^2 = -1 + (-1)*x + 1*x^2 = 0
# 따라서 c_0 = -1, c_1 = -1
char_poly = [-1, -1]

# 2. 초기 DP 배열 세팅 (O(K))
# F_0 = 0, F_1 = 1
initial_dp = [0, 1]

# 3. kitamasa 단독 호출로 x^N mod P(x)의 계수 도출 (O(K log K log N))
# coeffs = [r_0, r_1] 이 반환됨
coeffs = kitamasa(char_poly, N, K, MOD)

# 4. 계수와 초기 DP 값의 내적(Dot Product)으로 단일 항 복원 (O(K))
# F_N = r_0 * F_0 + r_1 * F_1
result = (coeffs[0] * initial_dp[0] + coeffs[1] * initial_dp[1]) % MOD

print(result)
"""