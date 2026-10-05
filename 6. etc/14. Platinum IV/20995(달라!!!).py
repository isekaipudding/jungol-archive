# 링크 : https://jungol.co.kr/problem/20995
import sys

input = sys.stdin.readline

MOD = 730391237
INV_2 = (MOD + 1) // 2

N, Q = map(int, input().split())
L:list = list(map(int, input().split()))

fact:list = [0 for _ in range(2 * N + 1)]
inv_fact:list = [0 for _ in range(2 * N + 1)]

# 초기식1
fact[0] = 1

# 점화식1
for i in range(1, 2 * N + 1, 1):
    fact[i] = (fact[i-1] * i) % MOD

# 초기식2
inv_fact[2 * N] = pow(fact[2 * N], MOD - 2, MOD)

# 점화식2
for i in range(2 * N, 0, -1):
    inv_fact[i - 1] = (inv_fact[i] * i) % MOD

invPow2:list = [0 for _ in range(N + 1)]

# 초기식3
invPow2[0] = 1

# 점화식3
for i in range(1, N + 1, 1):
    invPow2[i] = (invPow2[i-1] * INV_2) % MOD

for _ in range(Q):
    left, right = map(int, input().split())
    K:int = right - left + 1
    result:int = (1 - fact[2 * K] * invPow2[K] * (inv_fact[K]) ** 3) % MOD
    print(result)