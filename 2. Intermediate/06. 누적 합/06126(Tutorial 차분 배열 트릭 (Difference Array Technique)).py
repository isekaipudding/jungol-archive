# 링크 : https://jungol.co.kr/problem/6126
import sys

input = sys.stdin.readline

MAX_T = 1_000_000

N:int = int(input().rstrip())

diff:list = [0] * (MAX_T + 2)

for _ in range(N):
    S, E, C = map(int, input().split())
    
    diff[S] += C
    diff[E + 1] -= C

for i in range(1, MAX_T + 1, 1):
    diff[i] += diff[i - 1]

Q:int = int(input().rstrip())

for _ in range(Q):
    T:int = int(input().rstrip())
    print(diff[T])