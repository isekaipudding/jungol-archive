# 링크 : https://jungol.co.kr/problem/4726
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())
L:list = list(map(int, input().split()))

prefix:list = [0] * N

# 초기식
prefix[0] = L[0]

# 점화식
for i in range(1, N, 1):
    prefix[i] = prefix[i-1] + L[i]

total:int = prefix[-1]

result1:int = 0
for i in range(1, N - 1, 1):
    honey = 2 * total - L[0] - L[i] - prefix[i]
    result1 = max(result1, honey)

result2:int = 0
for i in range(1, N - 1, 1):
    honey = total - L[-1] - L[i] + prefix[i-1]
    result2 = max(result2, honey)

result3:int = 0
for i in range(1, N - 1, 1):
    honey = total - L[0] - L[-1] + L[i]
    result3 = max(result3, honey)

result:int = max(result1, result2, result3)
print(result)