# 링크 : https://jungol.co.kr/problem/8580
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())

vector:list = []

for _ in range(N):
    vector.append(list(map(int, input().split()))[1::])

L:list = list(map(int, input().split()))

for index in L:
    print(*vector[index])