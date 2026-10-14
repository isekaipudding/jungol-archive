# 링크 : https://jungol.co.kr/problem/8567
import sys

input = sys.stdin.readline

INF = 10 ** 18

N:int = int(input().rstrip())

min_y = INF
max_y = -INF

max_plus = -INF
min_plus = INF

max_minus = -INF
min_minus = INF

for _ in range(N):
    x, y = map(int, input().split())
    
    min_y = min(min_y, y)
    max_y = max(max_y, y)
    
    plus = y + x
    max_plus = max(max_plus, plus)
    min_plus = min(min_plus, plus)
    
    minus = y - x
    max_minus = max(max_minus, minus)
    min_minus = min(min_minus, minus)

case1 = max_plus + max_minus - 2 * min_y
case2 = 2 * max_y - min_plus - min_minus

print(min(case1, case2))