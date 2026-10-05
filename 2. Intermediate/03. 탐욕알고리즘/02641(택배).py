# 링크 : https://jungol.co.kr/problem/2641
import sys

input = sys.stdin.readline

N, C = map(int, input().split())
M:int = int(input().rstrip())

boxes:list = [None for _ in range(M)]

for i in range(M):
    query:list = list(map(int, input().split()))
    start, end, count = query[0], query[1], query[2]
    boxes[i] = (start, end, count)

boxes.sort(key=lambda x: (x[1], x[0]))

capacity:list = [C for _ in range(N + 1)]

result:int = 0

for start, end, box_count in boxes:
    TEMP = min(box_count, min(capacity[start:end]))
    
    if TEMP > 0:
        result += TEMP
        for i in range(start, end):
            capacity[i] -= TEMP

print(result)