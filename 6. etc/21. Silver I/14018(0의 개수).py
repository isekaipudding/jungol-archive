# 링크 : https://jungol.co.kr/problem/14018
import sys
import math

input = sys.stdin.readline

A, B = map(int, input().split())

pow_of_2, pow_of_5 = 0, 0
TWO, FIVE = 1, 1

while TWO < B:
    TWO *= 2
    pow_of_2 += 1

while FIVE < B:
    FIVE *= 5
    pow_of_5 += 1

while TWO > 1:
    status:bool = False
    for n in range(TWO * int(math.floor(A / TWO)), TWO * int(math.ceil(B / TWO)) + 1, TWO):
        if A <= n <= B:
            status = True
            break
    if status:
        break
    TWO //= 2
    pow_of_2 -= 1

while FIVE > 1:
    status:bool = False
    for n in range(FIVE * int(math.floor(A / FIVE)), FIVE * int(math.ceil(B / FIVE)) + 1, FIVE):
        if A <= n <= B:
            status = True
            break
    if status:
        break
    FIVE //= 5
    pow_of_5 -= 1

result:int = min(pow_of_2, pow_of_5)
print(result)