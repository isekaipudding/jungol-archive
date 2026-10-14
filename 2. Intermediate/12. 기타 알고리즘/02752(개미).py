# 링크 : https://jungol.co.kr/problem/2752
import sys

input = sys.stdin.readline

w, h = map(int, input().split())
p, q = map(int, input().split())
t:int = int(input().rstrip())

x = (p + t) % (2 * w)
x = 2 * w - x if x > w else x

y = (q + t) % (2 * h)
y = 2 * h - y if y > h else y

print(x, y)