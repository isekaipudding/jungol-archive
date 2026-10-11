# 링크 : https://jungol.co.kr/problem/3185
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())
K:int = int(input().rstrip())

L:list = [int(input().rstrip()) for _ in range(N)]
L.sort()

prefix:list = [0] * (N + 1)
for i in range(N):
    prefix[i + 1] = prefix[i] + L[i]

current_anger:int = 0
for i in range(K):
    current_anger += (2 * i - K + 1) * L[i]

min_anger:int = current_anger

# 슬라이딩 윈도우
for s in range(N - K):
    current_anger += (K - 1) * (L[s] + L[s + K]) - 2 * (prefix[s + K] - prefix[s + 1])
    min_anger = min(min_anger, current_anger)

print(min_anger)