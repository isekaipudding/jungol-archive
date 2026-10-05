# 링크 : https://jungol.co.kr/problem/1092
import sys

input = sys.stdin.readline

X, Y = map(int, input().split())
print(pow(X, Y, 20091024))