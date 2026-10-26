# 링크 : https://jungol.co.kr/problem/2902
import sys
from collections import Counter

input = sys.stdin.readline

N = input().rstrip()
C = Counter(N)
D = dict(C)

temp = 0
for k, v in D.items():
    temp += int(k) * v

# 예외 처리 1
if temp % 3:
    print(-1)
    sys.exit(0)

# 예외 처리 2
if not "0" in D:
    print(-1)
    sys.exit(0)

result = []

for k, v in D.items():
    result.append(k * v)

result.sort(key=lambda x: x[0], reverse=True)

print("".join(result))