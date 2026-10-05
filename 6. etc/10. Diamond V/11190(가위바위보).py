# 링크 : https://jungol.co.kr/problem/11190
import sys

input = sys.stdin.readline

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

N, M = map(int, input().split())
S:str = input().rstrip()
T:str = input().rstrip()[::-1]

# 기계가 가위(S)낼 때 바위(R)로 이기기
A:list = [0 for _ in range(N)]
B:list = [0 for _ in range(M)]
for i in range(N) :
    if S[i] == "S" :
        A[i] = 1
for i in range(M) :
    if T[i] == "R" :
        B[i] = 1
C1:list = multiply(A, B)

# 기계가 바위(R)낼 때 보(P)로 이기기
A:list = [0 for _ in range(N)]
B:list = [0 for _ in range(M)]
for i in range(N) :
    if S[i] == "R" :
        A[i] = 1
for i in range(M) :
    if T[i] == "P" :
        B[i] = 1
C2:list = multiply(A, B)

# 기계가 보(P)낼 때 가위(S)로 이기기
A:list = [0 for _ in range(N)]
B:list = [0 for _ in range(M)]
for i in range(N) :
    if S[i] == "P" :
        A[i] = 1
for i in range(M) :
    if T[i] == "S" :
        B[i] = 1
C3:list = multiply(A, B)

result:list = [0 for _ in range(len(C1))]

for i in range(len(C1)) :
    result[i] = C1[i] + C2[i] + C3[i]

print(max(result[M - 1 : N + M - 1 : 1]))