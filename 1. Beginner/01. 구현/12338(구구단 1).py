# 링크 : https://jungol.co.kr/problem/12338
import sys

input = sys.stdin.readline

A, B = map(int, input().split())

start, end, step = A, B, 0

if A <= B :
    end += 1
    step += 1
else :
    end -= 1
    step -= 1

for i in range(start, end, step) :
    for j in range(1, 10, 1) :
        print(f"{i} * {j} = {i * j}")
    print()