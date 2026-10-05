# 링크 : https://jungol.co.kr/problem/2498
import sys
import math

input = sys.stdin.readline

def gcd(a, b) :
    while b :
        a, b = b, a % b
    return a

GCD, LCM = map(int, input().split())
ab:int = LCM // GCD

"""
A = a * GCD
B = b * GCD
LCM = A * B / GCD
LCM = a * b * GCD

a * b = LCM / GCD <- 이거 채택
A * B = LCM * GCD
"""

# a * b에서 a는 LCM / GCD 이하 값을 가진다.
root:int = int(math.sqrt(ab))
a, b = root, root

# 제곱근 이하부터 시작하여 -1 만약 ab를 a로 딱 나누어 떨어지면서
# gcd(a, b) = 1이면 gcd(A, B) = GCD이면서 A, B의 차이가 최소화됩니다.
for n in range(root, 0, -1) :
    if ab % n == 0 :
        if gcd(n, ab // n) == 1 :
            a, b = n, ab // n
            break

print(a * GCD, b * GCD)