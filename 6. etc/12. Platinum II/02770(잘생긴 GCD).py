# 링크 : https://jungol.co.kr/problem/2770
import sys

input = sys.stdin.readline

def gcd(a, b):
    while b:
        a, b = b, a % b
    return a

N:int = int(input().rstrip())
L:list = list(map(int, input().split()))

result:int = 0

D:dict = dict()

for n in L:
    TEMP = dict()
    TEMP[n] = 1
    for k, v in D.items():
        GCD = gcd(k, n)
        TEMP[GCD] = max(TEMP.get(GCD, 0), v + 1)
    for k, v in TEMP.items():
        result = max(result, k * v)
    D = TEMP

print(result)