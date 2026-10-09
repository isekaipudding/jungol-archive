# 링크 : https://jungol.co.kr/problem/4803
import sys
import bisect

input = sys.stdin.readline

N, Q = map(int, input().split())

L:list = []

for _ in range(N):
    a, x = map(int, input().split())
    L.append((x, a))

L.sort(key=lambda x: x[0])

X:list = [item[0] for item in L]

prefix_a:list = [0] * (N + 1)
prefix_ax:list = [0] * (N + 1)

for i in range(N):
    x, a = L[i]
    prefix_a[i + 1] = prefix_a[i] + a
    prefix_ax[i + 1] = prefix_ax[i] + a * x

total_a:int = prefix_a[N]
total_ax:int = prefix_ax[N]

out = []
for _ in range(Q):
    q:int = int(input().rstrip())
    # 현재 쿼리 위치 q보다 작거나 같은 마을의 개수 k를 찾음
    k = bisect.bisect_right(X, q)
    
    # q보다 작거나 같은 마을들
    left_a = prefix_a[k]
    left_ax = prefix_ax[k]
    left_distance = q * left_a - left_ax
    
    # q보다 큰 마을들(전체 - 왼쪽 = suffix 효과)
    right_a = total_a - left_a
    right_ax = total_ax - left_ax
    right_distance = right_ax - q * right_a
    
    print(left_distance + right_distance)