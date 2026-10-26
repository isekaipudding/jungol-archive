# 링크 : https://jungol.co.kr/problem/4411
import sys

input = sys.stdin.readline

LIMIT = 30

fact:list = [0] * (LIMIT + 1)

# 초기식
fact[0] = 1

# 점화식
for i in range(1, LIMIT + 1, 1):
    fact[i] = i * fact[i - 1]

def coff(n, k):
    return fact[n] // fact[k] // fact[n - k]

N, K = map(int, input().split())

print(coff(N, K))