# 링크 : https://jungol.co.kr/problem/1692
import sys

input = sys.stdin.readline

A:int = int(input().rstrip())
B:str = input().rstrip()

for i in range(len(B)-1, -1, -1) :
    print(A * int(B[i]))

B = int(B)

print(A * B)