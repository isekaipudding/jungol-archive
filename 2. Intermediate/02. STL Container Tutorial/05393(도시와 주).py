# 링크 : https://jungol.co.kr/problem/5393
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())

D:dict = dict()
for _ in range(N):
    city, code = map(str, input().split())
    city = city[0:2:1]
    if city == code:
        continue
    if (city, code) not in D:
        D[(city, code)] = 1
    else:
        D[(city, code)] += 1

S:set = set()

result:int = 0
for a, b in D.keys():
    if (a, b) not in S:
        if (b, a) in D:
            result += D[(a, b)] * D[(b, a)]
            S.add((a, b))
            S.add((b, a))

print(result)