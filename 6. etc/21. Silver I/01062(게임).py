# 링크 : https://jungol.co.kr/problem/1062
import sys

input = sys.stdin.readline

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

N, A, B = map(int, input().split())

GCD = gcd(A, B)
MAX = max(A, B)

K = (MAX // GCD) - 2

winner = (K - 1) % N + 1

print(winner)