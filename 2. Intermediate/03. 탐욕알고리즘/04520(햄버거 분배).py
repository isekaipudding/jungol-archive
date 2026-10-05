# 링크 : https://jungol.co.kr/problem/4520
import sys

input = sys.stdin.readline

N, K = map(int, input().split())
HP = input().rstrip()
L:list = [0 for _ in range(N)]

for i in range(N):
    if HP[i] == "H":
        L[i] = 1
    if HP[i] == "P":
        L[i] = 2

result:int = 0

# 여기가 그리디 알고리즘
# 스위핑 알고리즘으로 가장 왼쪽의 사람이 무조건 가장 왼쪽에 있는 햄버거를 먹는 방식으로 합니다.
for i in range(N):
    if L[i] == 2:
        for j in range(max(0, i - K), min(N - 1, i + K) + 1, 1):
            if L[j] == 1:
                L[j] = 0
                result += 1
                break

print(result)