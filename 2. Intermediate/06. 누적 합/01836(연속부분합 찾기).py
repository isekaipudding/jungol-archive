# 링크 : https://jungol.co.kr/problem/1836
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())
L:list = list(map(int, input().split()))

result:int = 0
current:int = 0

for x in L:
    current = max(0, current + x)
    result = max(result, current)

print(result)