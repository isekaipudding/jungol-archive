# 링크 : https://jungol.co.kr/problem/4987
import sys

input = sys.stdin.readline

S:str = input().rstrip()
T:str = input().rstrip()

index:int = 0

while index != -1 :
    index = S.find(T)
    if index != -1 :
        S = S[0:index:1] + S[index + len(T)::]

print(S)