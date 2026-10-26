# 링크 : https://jungol.co.kr/problem/12365
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())
L:list = [0] + list(map(int, input().split()))

left = [0 for _ in range(N + 1)]
right = [0 for _ in range(N + 1)]

# 초기식
left[0] = 0
right[N] = L[N]

# 점화식 1
for i in range(1, N + 1, 1):
    left[i] = max(left[i-1] + L[i], L[i])

# 점화식 2
for i in range(N - 1, 0, -1):
    right[i] = max(right[i+1] + L[i], L[i])

result:list = [left[i] + right[i] - L[i] for i in range(1, N + 1, 1)]

print(*result)