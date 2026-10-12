# 링크 : https://jungol.co.kr/problem/5628
import sys

input = sys.stdin.readline

N, H = map(int, input().split())

diff:list = [0] * (H + 2)

for i in range(N):
    L:int = int(input().rstrip())
    
    if i & 1:
        diff[H - L + 1] += 1
        diff[H + 1] -= 1
    else:
        diff[1] += 1
        diff[L + 1] -= 1

min_count:int = N + 1
height_frequency:int = 0

current_obstacles = 0
for height in range(1, H + 1, 1):
    current_obstacles += diff[height]
    
    if current_obstacles < min_count:
        min_count = current_obstacles
        height_frequency = 1
    elif current_obstacles == min_count:
        height_frequency += 1
    
print(min_count, height_frequency)