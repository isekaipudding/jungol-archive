# 링크 : https://jungol.co.kr/problem/8559
import sys

input = sys.stdin.readline

L:list = list(map(int, input().split()))

result:list = [n + 1 for n in L]
result.sort()
print(*result)