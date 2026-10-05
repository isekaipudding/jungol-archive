# 링크 : https://jungol.co.kr/problem/2499
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())
L:list = list(map(int, input().split()))

L.sort()

result:int = 1

for i in range(N):
    weight:int = L[i]
    
    if weight <= result:
        result += weight
    else:
        break

print(result)