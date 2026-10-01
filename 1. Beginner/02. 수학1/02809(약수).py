# 링크 : https://jungol.co.kr/problem/2809
import sys
import math

input = sys.stdin.readline

S:set = set()

N:int = int(input().rstrip())

for i in range(1, int(math.sqrt(N))+1, 1) :
    if N % i == 0 :
        S.add(i)
        S.add(N // i)
        
L:list = list(S)
L.sort()

print(*L)