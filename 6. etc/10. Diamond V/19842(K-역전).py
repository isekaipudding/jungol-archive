# 링크 : https://jungol.co.kr/problem/19842
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

K:str = input().rstrip()

N:int = len(K)

A:list = [0 for _ in range(N)]
B:list = [0 for _ in range(N)]

for i in range(N):
    # 일단 해당 index에 A 혹은 B가 있으면 무조건 1을 넣어줍니다.
    if K[i] == "A":
        A[i] = 1
    if K[i] == "B":
        B[i] = 1

# 두 자리수의 곱셈식에서 살짝 비틀어서 연산합니다.
B.reverse()

C:list = multiply(A, B)[N:2*N:1]

for result in C:
    print(result)