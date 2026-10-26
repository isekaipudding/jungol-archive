# 링크 : https://jungol.co.kr/problem/1057
import sys
import math

input = sys.stdin.readline
isqrt = math.isqrt

S:int = int(input().rstrip())

# N = {root(8S + 1) - 1} / 2이므로
# 2 * N - 1 >= root(8S + 1)

value = 8 * S + 1
root = isqrt(value)

if root * root < value:
    root += 1

N:int = root // 2
print(N)