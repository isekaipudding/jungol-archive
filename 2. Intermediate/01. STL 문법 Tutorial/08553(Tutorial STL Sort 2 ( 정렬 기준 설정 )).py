# 링크 : https://jungol.co.kr/problem/8553
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())

L:list = ["" for _ in range(N)]

for i in range(N) :
    L[i] = input().rstrip()

L.sort(key=lambda x: (x[2], x[1], x[0]))

for number in L :
    print(number)