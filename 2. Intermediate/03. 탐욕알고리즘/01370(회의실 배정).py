# 링크 : https://jungol.co.kr/problem/1370
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())

L:list = [[0, 0, 0] for _ in range(N)]

for i in range(N) :
    L[i][0], L[i][1], L[i][2] = map(int, input().split())

L.sort(key=lambda x:x[1])
L.sort(key=lambda x:x[2])

rooms_count:int = 1
current_end:int = L[0][2]
rooms_list:list = [L[0][0]]

for i in range(1, N, 1) :
    if L[i][1] >= current_end :
        rooms_count += 1
        current_end = L[i][2]
        rooms_list.append(L[i][0])

print(rooms_count)
print(*rooms_list)