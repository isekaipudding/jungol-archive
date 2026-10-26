# 링크 : https://jungol.co.kr/problem/2303
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())
L:list = list(map(int, input().split()))
L.sort()

result = float('inf')
A, B, C = float('inf'), float('inf'), float('inf')

for i in range(N - 2):
    start = i + 1
    end = N - 1
    
    while start < end:
        TEMP = L[i] + L[start] + L[end]

        if abs(TEMP) < result:
            result = abs(TEMP)
            A, B, C = L[i], L[start], L[end]

        if TEMP == 0:
            break
        if TEMP < 0:
            start += 1
        else:
            end -= 1

print(A, B, C)