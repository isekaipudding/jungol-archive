# 링크 : https://jungol.co.kr/problem/3336
import sys

input = sys.stdin.readline

# 좌표 범위 -500,000 ~ 500,000 -> 0 ~ 1,000,000으로 평행이동
OFFSET = 500000
MAX_COORD = 1000000

N:int = int(input().rstrip())

diff_h:list = [0] * (MAX_COORD + 2)
diff_v:list = [0] * (MAX_COORD + 2)

# 꼭짓점 파싱(n개의 점)
xs:list = [0] * N
ys:list = [0] * N

for i in range(N):
    x, y = map(int, input().split())
    xs[i], ys[i] = x + OFFSET, y + OFFSET
    
# 다각형의 n개 변 순회(i와 (i + 1) % n)
for i in range(N):
    next_index = (i + 1) % N
    x1, y1 = xs[i], ys[i]
    x2, y2 = xs[next_index], ys[next_index]
    
    if x1 == x2:
        # 1. 수직선분 : 수평선 H와의 교차 대상
        y_low = min(y1, y2)
        y_high = max(y1, y2)
        # 단위 구간 [y_low, y_high - 1]에 +1
        diff_h[y_low] += 1
        diff_h[y_high] -= 1
    else:
        # 2. 수평선분 : 수직선 V와의 교차 대상
        x_low = min(x1, x2)
        x_high = max(x1, x2)
        # 단위 구간 [x_low, x_high - 1]에 +1
        diff_v[x_low] += 1
        diff_v[x_high] -= 1
        
# 누적합으로 최대 교차 횟수 h, v 계산
# current 대신 cur로 줄입니다.
max_h = 0
cur_h = 0
for value in diff_h:
    cur_h += value
    max_h = max(max_h, cur_h)
        
max_v = 0
cur_v = 0
for value in diff_v:
    cur_v += value
    max_v = max(max_v, cur_v)
        
print(max(max_h, max_v))