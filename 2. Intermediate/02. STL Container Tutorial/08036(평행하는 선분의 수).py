# 링크 : https://jungol.co.kr/problem/8036
import sys

input = sys.stdin.readline

def sigma(N:int):
    return N * (N + 1) // 2

X, Y = dict(), dict()

N:int = int(input().rstrip())

for _ in range(N):
    x, y = map(int, input().split())
    
    if x not in X:
        X[x] = 1
    else:
        X[x] += 1
    if y not in Y:
        Y[y] = 1
    else:
        Y[y] += 1

result:int = 0

for x in X.keys():
    result += sigma(X[x] - 1)
for y in Y.keys():
    result += sigma(Y[y] - 1)

print(result)