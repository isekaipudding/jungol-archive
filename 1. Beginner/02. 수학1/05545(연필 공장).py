# 링크 : https://jungol.co.kr/problem/5545
import sys

input = sys.stdin.readline

def gcd(a, b) :
    while b :
        a, b = b, a % b
    return a

P, V, K = map(int, input().split())
P += 1
V += 1
LCM:int = P * V // gcd(P, V)

A, B, C, D = 0, 0, 0, 0

# 도색도 광택도 되지 않는 경우
B = K // LCM
# 도색은 되었으나 광택이 되지 않는 경우(포함 배제의 원리)
C = K // V - B
# 광택은 되었으나 도색이 되지 않는 경우(포함 배제의 원리)
D = K // P - B
# 도색과 광택이 완료된 경우
A = K - B - C - D

print(A, B, C, D)