# 링크 : https://jungol.co.kr/problem/1307
import sys

input = sys.stdin.readline

# 런타임 전처리(캐시 기능)
D:dict = dict()
for i in range(65, 65 + 26, 1) :
    D[i - 65] = chr(i)

N:int = int(input().rstrip())

for i in range(1, N + 1, 1) :
    L:list = [D[(N * j - i) % 26] for j in range(N, 0, -1)]
    print(*L)