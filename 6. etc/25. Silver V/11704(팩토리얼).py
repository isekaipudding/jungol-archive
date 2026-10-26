# 링크 : https://jungol.co.kr/problem/11704
import sys

input = sys.stdin.readline

T:int = int(input().rstrip())

for _ in range(T):
    N:int = int(input().rstrip())

    result = 0
    TEMP = 5

    while TEMP <= N:
        result += N // TEMP
        TEMP *= 5

    print(result)