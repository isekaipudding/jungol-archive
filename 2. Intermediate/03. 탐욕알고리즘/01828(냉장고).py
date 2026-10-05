# 링크 : https://jungol.co.kr/problem/1828
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())

chemicals = [None for _ in range(N)]
for i in range(N):
    x, y = map(int, input().split())
    chemicals[i] = (x, y)

chemicals.sort(key=lambda x: x[1])

count:int = 1

current_temp:int = chemicals[0][1]

for i in range(1, N, 1):
    min_temp, max_temp = chemicals[i]
    
    if min_temp > current_temp:
        count += 1
        current_temp = max_temp
        
print(count)