# 링크 : https://jungol.co.kr/problem/3706
import sys
from collections import Counter

input = sys.stdin.readline

def sigma(N:int) :
    return (N + 1) * N // 2

N:int = int(input().rstrip())
L:list = list(map(int, input().split()))

prefix:list = [0 for _ in range(N + 1)]

for i in range(1, N + 1, 1) :
    prefix[i] = prefix[i-1] + L[i-1]

C:Counter = Counter(prefix)

result:int = 0

for k, v in C.items() :
    result += sigma(v - 1)

print(result)