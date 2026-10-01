# 링크 : https://jungol.co.kr/problem/1402
import sys
import math

input = sys.stdin.readline

S:set = set()

N, K = map(int, input().split())

for i in range(1, int(math.sqrt(N))+1, 1) :
    if N % i == 0 :
        S.add(i)
        S.add(N // i)
        
L:list = list(S)
L.sort()

if K <= len(L) :
    print(L[K-1])
else :
    print(0)