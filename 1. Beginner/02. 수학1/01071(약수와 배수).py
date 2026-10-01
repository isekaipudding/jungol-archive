# 링크 : https://jungol.co.kr/problem/1071
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())
L:list = list(map(int, input().split()))
M:int = int(input().rstrip())

result:int = 0
for i in range(N) :
    if M % L[i] == 0 :
        result += L[i]
print(result)

result = 0
for i in range(N) :
    if L[i] % M == 0 :
        result += L[i]
print(result)