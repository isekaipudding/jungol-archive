# 링크 : https://jungol.co.kr/problem/19405
import sys
import heapq

input = sys.stdin.readline

# 에디토리얼 : https://static.ucpc.me/files/2021/ucpc21-prelim-solutions.pdf

N:int = int(input().rstrip())
S:str = input().rstrip()
A:list = list(map(int, input().split()))

TEMP = 0
status = False
pq = []

for i in range(N):
    if i == 0:
        continue
    if S[i] != S[i - 1]:
        if status:
            heapq.heappush(pq, -TEMP)
        else:
            status = True
        TEMP = 0
    TEMP = max(TEMP, A[i])

result:int = 0
for _ in range((len(pq) + 1) >> 1):
    result += -heapq.heappop(pq)

print(result)