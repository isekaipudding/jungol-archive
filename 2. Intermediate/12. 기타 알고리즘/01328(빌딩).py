# 링크 : https://jungol.co.kr/problem/1328
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())
heights:list = [int(input().rstrip()) for _ in range(N)]

stack = []
result:list = [0] * N

# 역순으로 진행해야 합니다.
for i in range(N - 1, -1, -1):
    h = heights[i]
    while stack and stack[-1][1] <= h:
        stack.pop()
    
    if stack:
        result[i] = stack[-1][0]
    else:
        result[i] = 0

    # 1-based index로 해야 하네요.
    stack.append((i + 1, h))

for number in result:
    print(number)