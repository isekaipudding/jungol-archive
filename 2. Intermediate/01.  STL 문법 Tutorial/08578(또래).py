# 링크 : https://jungol.co.kr/problem/8578
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())

L:list = list(map(int, input().split()))
L.sort()

result:int = 10 ** 9

for i in range(N-1) :
    result = min(result, L[i+1] - L[i])

print(result)