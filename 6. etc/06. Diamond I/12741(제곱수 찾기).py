# 링크 : https://jungol.co.kr/problem/12741
import sys
import math

input = sys.stdin.readline

# 와 미친 난이도 너무 높네 뭐 이렇게 복잡한 수식들이 많이 등장하는지 참...
# 조금만 더 복잡했다면 루비 5티어 이상 갈 것 같네요.

MOD = 1_000_000_007
LIMIT = 1_000_000

# 출처 : https://en.wikipedia.org/wiki/Tonelli%E2%80%93Shanks_algorithm
def tonelli_shanks(n:int, p:int) -> int:
    # 이차 잉여 (Quadratic Residue)와 르장드르 기호 (Legendre Symbol)
    # 홀수 소수 p에 대하여 x^2 = n (mod p)를 만족하는 이산 제곱근 x를 반환한다.
    n %= p
    if n == 0:
        return 0
    if p == 2:
        return n
    
    # 오일러 판별법 (Euler's Criterion) : 근이 존재하는지 검사
    if pow(n, (p - 1) >> 1, p) != 1:
        return -1

    if p & 3 == 3:
        return pow(n, (p + 1) >> 2, p)

    q = p - 1
    s = 0
    while q & 1 == 0:
        q >>= 1
        s += 1

    z = 2
    while pow(z, (p - 1) >> 1, p) != p - 1:
        z += 1

    m = s
    c = pow(z, q, p)
    t = pow(n, q, p)
    r = pow(n, (q + 1) >> 1, p)

    while t != 1:
        tt = t
        i = 0
        while tt != 1:
            tt = (tt * tt) % p
            i += 1
        b_v = pow(c, 1 << (m - i - 1), p)
        m = i
        c = (b_v * b_v) % p
        t = (t * c) % p
        r = (r * b_v) % p

    return r

def get_polynomial_roots(a:int, b:int, c:int, p:int) -> list:
    # 유한체(Finite Field) 상에서의 이차방정식의 해(근의 공식)
    # a*x^2 + b*x + c = 0 (mod p)의 해집합을 반환합니다.
    if p == 2:
        roots = []
        if c & 1 == 0:
            roots.append(0)
        if (a + b + c) & 1 == 0:
            roots.append(1)
        return roots

    # 모듈러 연산에서의 나눗셈 
    # 역원을 이용해 1차 방정식 해 구하기
    if a % p == 0:
        if b % p == 0:
            return list(range(p)) if c % p == 0 else []
        return [(-c * pow(b, -1, p)) % p]

    disc = (b * b - 4 * a * c) % p
    
    # 모듈러 곱셈 역원
    inv_2a = pow(2 * a, -1, p)

    if disc == 0:
        return [(-b * inv_2a) % p]

    sqrt_d = tonelli_shanks(disc, p)
    if sqrt_d == -1:
        return []

    r1 = ((-b + sqrt_d) * inv_2a) % p
    r2 = ((-b - sqrt_d) * inv_2a) % p
    return [r1] if r1 == r2 else [r1, r2]

def eratosthenes_sieve(n:int) -> list :
    if n < 2 :
        return []
    
    is_prime:list = [True] * (n + 1)
    
    is_prime[0], is_prime[1] = False, False
    
    for i in range(4, n + 1, 2) :
        is_prime[i] = False
        
    for i in range(3, int(math.sqrt(n)) + 1, 2) :
        if is_prime[i] :
            for j in range(i * i, n + 1, 2 * i) :
                is_prime[j] = False
                
    return [index for index, value in enumerate(is_prime) if value]

a, b, c, n = map(int, input().split())

vs = [a * x * x + b * x + c for x in range(n)]
primes = eratosthenes_sieve(LIMIT)

half_prod = 1

# 1. LIMIT 이하의 소수에 대한 다항식 체
# 다항식 체(Polynomial Sieve)
# 모든 x에 대해 함숫값을 각각 소인수분해하면 O(N * sqrt(V))로 시간초과가 발생.
# 대신 p(x) ≡ 0 (mod p)가 되는 근(r)을 먼저 찾고, r부터 시작해 p씩 건너뛰며(x = r + k*p)
# 나누어 주는 기법. O(N log log N) 수준으로 최적화.
for p in primes:
    roots = get_polynomial_roots(a, b, c, p)
    if not roots:
        continue
    count = 0
    for r in roots:
        for i in range(r, n, p):
            v = vs[i]
            while v % p == 0:
                v //= p
                count += 1
            vs[i] = v
    if count >= 2:
        half_prod = (half_prod * pow(p, count >> 1, MOD)) % MOD

# 2. L(s) = a*s + b 선형 체를 통한 큰 합성수 쌍의 공통 소인수 추출
if n >= 2:
    max_s: int = 2 * n - 3
    # 대수적 조작(Algebraic Manipulation) 그리고 모듈러 합동성
    # p(x2) - p(x1) = a(x2^2 - x1^2) + b(x2 - x1) = (x2 - x1) * (a(x2 + x1) + b)
    # 두 식을 동시에 나누는 큰 소수 q는 반드시 a(x1+x2)+b 꼴을 나누어야 한다는 성질 유도
    l = [a * s + b for s in range(max_s + 1)]

    # 선형 체(Linear Sieve) 응용
    # 1차 방정식 L(s) = a*s + b 의 값을 소수 p로 체질하여, LIMIT 이상의 거대한 소수를 필터링
    for p in primes:
        if a % p == 0:
            if b % p == 0:
                for s in range(1, max_s + 1):
                    v = l[s]
                    while v % p == 0:
                        v //= p
                    l[s] = v
            continue

        s0: int = (-b * pow(a, -1, p)) % p
        if s0 == 0:
            s0 = p
        for s in range(s0, max_s + 1, p):
            v = l[s]
            while v % p == 0:
                v //= p
            l[s] = v

    cand_primes = set()
    for s in range(1, max_s + 1):
        q = l[s]
        if q > LIMIT:
            # 합성수 필터링을 위한 부등식 한계(Bound) 검사
            half_s = (s - 1) >> 1
            max_p_x1 = a * half_s * half_s + b * half_s + c
            if max_p_x1 > LIMIT * q:
                cand_primes.add(q)

    # 추출된 거대 소수 후보들만 대상으로 다시 다항식 체(Polynomial Sieve) 적용
    for q in cand_primes:
        roots = get_polynomial_roots(a, b, c, q)
        if not roots:
            continue
        count = 0
        for r in roots:
            if r < n:
                v = vs[r]
                while v % q == 0:
                    v //= q
                    count += 1
                vs[r] = v
        if count >= 2:
            half_prod = (half_prod * pow(q, count >> 1, MOD)) % MOD

# 3. 남은 값들에서 완전제곱수 및 근과 계수의 관계를 통한 단일 소수 매칭
for x in range(n):
    v = vs[x]
    if v <= 1:
        continue

    # 정수 제곱근(Integer Square Root)
    # 부동소수점 오차(Precision Error)를 회피하기 위해 실수 연산을 배제하고 정수 제곱근을 추출합니다.
    rt = math.isqrt(v)
    if rt * rt == v:
        half_prod = (half_prod * (rt % MOD)) % MOD
        vs[x] = 1
        continue

    # 유한체 상의 근과 계수의 관계(Vieta's Formulas over Finite Fields)
    # 이차방정식에서 한 근 x1을 알고 있을 때, 두 근의 합 x1 + x2 ≡ -b/a (mod p) 임을 이용하여
    # 이산 제곱근 같은 무거운 연산 없이, O(1) 만에 나머지 짝꿍 해(x2)를 즉시 특정합니다.
    inv_a = pow(a, -1, v)
    y = (-x - b * inv_a) % v
    if x < y < n and vs[y] % v == 0:
        half_prod = (half_prod * (v % MOD)) % MOD
        vs[x] = 1
        vs[y] //= v

result:int = (half_prod * half_prod) % MOD
print(result)