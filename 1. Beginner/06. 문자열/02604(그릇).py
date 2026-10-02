# 링크 : https://jungol.co.kr/problem/2604
import sys

input = sys.stdin.readline

plates:str = input().rstrip()
current:str = ""

result:int = 0
for plate in plates :
    if plate == current :
        result += 5
    else :
        result += 10
        current = plate

print(result)