# 링크 : https://jungol.co.kr/problem/2461
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())
L:list = [[0, 0] for _ in range(N)]

for i in range(N):
    a, b, c, d = map(int, input().split())
    L[i][0], L[i][1] = 100 * a + b, 100 * c + d

# 그리디 적용하기 위해 피는 날짜 기준으로 오름차순 정렬하고 피는 날짜가 같은 경우 지는 날짜를 내림차순으로 정렬합니다.
L.sort(key=lambda x: (x[0], -x[1]))

current_end:int = 301
result:int = 0
index:int = 0

while current_end <= 1130:
    next_end = current_end
    
    for i in range(index, N, 1):
        if L[i][0] <= current_end:
            next_end = max(next_end, L[i][1])
            index += 1
        else:
            break
    if current_end == next_end:
        result = 0
        break
    
    current_end = next_end
    result += 1

print(result)