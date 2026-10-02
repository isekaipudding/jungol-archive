# 링크 : https://jungol.co.kr/problem/2814
import sys

input = sys.stdin.readline

binary:str = input().rstrip()

shift:int = 1
result:int = 0
for i in range(len(binary)-1, -1, -1) :
    result += shift * int(binary[i])
    shift <<= 1
    
print(result)