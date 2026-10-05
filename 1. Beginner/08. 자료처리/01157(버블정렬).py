# 링크 : https://jungol.co.kr/problem/1157
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())
L:list = list(map(int, input().split()))

for _ in range(N-1) :
    for i in range(1, N, 1) :
        if L[i-1] > L[i] :
            L[i-1], L[i] = L[i], L[i-1]
    print(*L)