# 링크 : https://jungol.co.kr/problem/1141
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())
heights:list = [int(input().rstrip()) for _ in range(N)]

stack = []
total_count = 0

for h in heights:
    while stack and stack[-1] <= h:
        stack.pop()
    total_count += len(stack)
    stack.append(h)

print(total_count)