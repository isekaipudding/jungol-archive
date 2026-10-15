# 링크 : https://jungol.co.kr/problem/3232
import sys

input = sys.stdin.readline

def cross(start_a, end_a, start_b, end_b):
    left = max(start_a, start_b)
    right = min(end_a, end_b)
    
    if left > right:
        return -1
    elif left == right:
        return 0
    else:
        return 1

px1, py1, px2, py2 = map(int, input().split())
qx1, qy1, qx2, qy2 = map(int, input().split())

state_x = cross(px1, px2, qx1, qx2)
state_y = cross(py1, py2, qy1, qy2)

if state_x == -1 or state_y == -1:
    print("NULL")
elif state_x == 1 and state_y == 1:
    print("FACE")
elif state_x == 0 and state_y == 0:
    print("POINT")
else:
    print("LINE")