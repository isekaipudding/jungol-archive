# 링크 : https://jungol.co.kr/problem/1158
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())
L:list = list(map(int, input().split()))

start:int = 1

for _ in range(N-1) :
    for i in range(start, 0, -1) :
        if L[i-1] > L[i] :
            L[i-1], L[i] = L[i], L[i-1]
        else :
            break
    print(*L)
    start += 1