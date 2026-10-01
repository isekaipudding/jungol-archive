# 링크 : https://jungol.co.kr/problem/1002
import sys

input = sys.stdin.readline

def gcd(a, b) :
    while b :
        a, b = b, a % b
    return a

def lcm(a, b) :
    return a * b // gcd(a, b)

N:int = int(input().rstrip())
L:list = list(map(int, input().split()))

GCD, LCM = L[0], L[0]

for num in L :
    GCD, LCM = gcd(GCD, num), lcm(LCM, num)

print(GCD, LCM)