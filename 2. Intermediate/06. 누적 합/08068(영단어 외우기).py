# 링크 : https://jungol.co.kr/problem/8068
import sys

input = sys.stdin.readline

N, M, Q = map(int, input().split())
A:list = [0] + list(map(int, input().split()))

diff:list = [0] * (N + 10005)

for i in range(1, N + 1, 1):
    words = A[i]
    d, r = words // M, words % M
    
    if d:
        diff[i + 1] += M
        diff[i + d + 1] -= M
    if r:
        diff[i + d + 1] += r
        diff[i + d + 2] -= r

forgotten:list = [0] * (N + 1)
current_forgotten:int = 0
for t in range(1, N + 1, 1):
    current_forgotten += diff[t]
    forgotten[t] = current_forgotten

remembered:list = [0] * (N + 1)
for t in range(1, N + 1, 1):
    remembered[t] = remembered[t - 1] - forgotten[t] + A[t]

for _ in range(Q):
    query:list = list(map(int, input().split()))
    cmd, t = query[0], query[1]
    
    if cmd == 1:
        print(remembered[t])
    if cmd == 2:
        print(forgotten[t])