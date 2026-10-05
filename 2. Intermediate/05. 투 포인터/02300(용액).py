# 링크 : https://jungol.co.kr/problem/2300
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())
L:list = list(map(int, input().split()))
L.sort()

start, end = 0, N - 1
A, B = L[start], L[end]
result:int = float('inf')

while start < end:
    TEMP = L[start] + L[end]
    if abs(TEMP) < result:
        result = abs(TEMP)
        A, B = L[start], L[end]
    if TEMP == 0:
        break
    if TEMP < 0:
        start += 1
    else:
        end -= 1

print(A, B)