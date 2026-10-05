# 링크 : https://jungol.co.kr/problem/8551
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())
L:list = list(map(int, input().split()))
x, y = map(int, input().split())

L[x:y+1:1] = sorted(L[x:y+1:1])
print(*L)

L.sort()
print(*L)