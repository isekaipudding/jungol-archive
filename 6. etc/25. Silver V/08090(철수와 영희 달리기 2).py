# 링크 : https://jungol.co.kr/problem/8090
import sys

input = sys.stdin.readline

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

N:int = int(input().rstrip())

Ax, Ay = map(int, input().split())
Bx, By = map(int, input().split())

A, B = 2 * (Ax + Ay), 2 * (Bx + By)

LCM = A // gcd(A, B) * B

result:int = N * A // LCM

print(result)