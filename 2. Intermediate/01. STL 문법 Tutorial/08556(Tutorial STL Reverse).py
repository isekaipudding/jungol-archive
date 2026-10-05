# 링크 : https://jungol.co.kr/problem/8556
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())
L:list = list(map(int, input().split()))
X, Y = map(int, input().split())

TEMP:list = L[X:Y+1:1]
TEMP.reverse()
L[X:Y+1:1] = TEMP
print(*L)

L.sort(reverse=True)
print(*L)