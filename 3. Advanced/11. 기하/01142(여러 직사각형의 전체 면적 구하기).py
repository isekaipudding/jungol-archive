# 링크 : https://jungol.co.kr/problem/1142
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())

rectangles:list = []
x_coords:set = set()
for _ in range(N):
    x1, y1, w, h = map(float, input().split())
    x1 = round(10 * x1)
    y1 = round(10 * y1)
    w = round(10 * w)
    h = round(10 * h)
    
    x2 = x1 + w
    y2 = y1 + h
    
    rectangles.append((x1, y1, x2, y2))
    x_coords.add(x1)
    x_coords.add(x2)

sorted_x:list = sorted(x_coords)
result:int = 0

for i in range(len(sorted_x) - 1):
    x_left = sorted_x[i]
    x_right = sorted_x[i + 1]
    dx = x_right - x_left
    
    active_y = [
        (y1, y2) for rx1, y1, rx2, y2 in rectangles
        if rx1 <= x_left and rx2 >= x_right
    ]
    
    if not active_y:
        continue
    
    active_y.sort()
    y_len = 0
    current_y1, current_y2 = active_y[0]
    
    for i in range(1, len(active_y), 1):
        ny1, ny2 = active_y[i][0], active_y[i][1]
        
        if ny1 <= current_y2:
            current_y2 = max(current_y2, ny2)
        else:
            y_len += current_y2 - current_y1
            current_y1, current_y2 = ny1, ny2
    y_len += current_y2 - current_y1
    
    result += dx * y_len

if result % 100 == 0:
    print(result // 100)
else:
    print(f"{result / 100:.2f}")