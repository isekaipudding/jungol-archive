# 링크 : https://jungol.co.kr/problem/2089
import sys

input = sys.stdin.readline

a, b = map(int, input().split())

for k in range(40, 0, -1):
    x = int(b ** (1 / k)) # b의 k제곱근(내림)
    
    # 부동소수점 오차 보정
    while (x + 1) ** k <= b:
        x += 1
    while x ** k > b:
        x -= 1
        
    # 구간 하한선(a)만 넘으면 무조건 구간 내에 존재합니다!
    if x ** k >= a:
        print(k)
        break