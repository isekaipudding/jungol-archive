# 링크 : https://jungol.co.kr/problem/1618
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())

code = bin(N)[2:]
size = len(code)

shift = 1
result:int = 0

for i in range(size - 1, -1, -1):
    result += shift * int(code[i])
    shift *= 3

print(result)