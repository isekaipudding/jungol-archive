# 링크 : https://jungol.co.kr/problem/5445
import sys

input = sys.stdin.readline

N = int(input().rstrip())
C = list(map(int, input().split()))

total_sum = sum(C)
q = total_sum // N

# D: q 미만인 사람들이 반드시 받아야 하는 최소 금액
# E: q + 1 초과인 사람들이 반드시 주어야 하는 최소 금액
deficit = 0
excess = 0

for x in C:
    if x < q:
        deficit += q - x
    elif x > q + 1:
        excess += x - (q + 1)

result = max(deficit, excess)
print(result)