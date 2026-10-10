# 링크 : https://jungol.co.kr/problem/8691
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())
L:list = list(map(int, input().split()))

count:int = 0
S:set = set()

current:int = 0

for number in L:
    if number != current:
        count += 1
        S.add(number)
        current = number

print(count, len(S))