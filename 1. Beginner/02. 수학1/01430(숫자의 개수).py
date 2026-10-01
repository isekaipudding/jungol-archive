# 링크 : https://jungol.co.kr/problem/1430
import sys

input = sys.stdin.readline

L:list = [0] * 10

A:int = int(input().rstrip())
B:int = int(input().rstrip())
C:int = int(input().rstrip())

X:str = str(A * B * C)

for i in range(len(X)) :
    L[int(X[i])] += 1
    
for i in range(10) :
    print(L[i])