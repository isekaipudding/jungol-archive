# 링크 : https://jungol.co.kr/problem/1408
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())

wires:list = []
for _ in range(N):
    a, b = map(int, input().split())
    wires.append((a, b))

wires.sort(key=lambda x: x[0])

B:list = [wire[1] for wire in wires]

dp:list = [1] * N

# 점화식
for i in range(N):
    for j in range(i):
        if B[j] < B[i]:
            dp[i] = max(dp[i], dp[j] + 1)

max_connected = max(dp) if N > 0 else 0

print(N - max_connected)