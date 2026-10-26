# 링크 : https://jungol.co.kr/problem/1040
import sys

input = sys.stdin.readline

N, M = map(str, input().split())
A, B = len(N), len(M)
size:int = max(A, B)

N = "0" * (size - A) + N
M = "0" * (size - B) + M

carry:int = 0
result:int = 0

for i in range(size-1, -1, -1) :
    TEMP:int = int(N[i]) + int(M[i]) + carry
    if TEMP >= 10 :
        carry = 1
        result += 1
    else :
        carry = 0

if result :
    if result == 1 :
        print(f"{result} carry operation.")
    elif result >= 1 :
        print(f"{result} carry operations.")
        
else :
    print("No carry operation.")