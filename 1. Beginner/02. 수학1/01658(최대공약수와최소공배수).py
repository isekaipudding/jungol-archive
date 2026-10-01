# 링크 : https://jungol.co.kr/problem/1658
import sys

input = sys.stdin.readline

def gcd(a, b) :
    while b :
        a, b = b, a % b
    return a

A, B = map(int, input().split())
GCD:int = gcd(A, B)
print(GCD)
print(A * B // GCD)