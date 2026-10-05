# 링크 : https://jungol.co.kr/problem/8576
import sys

input = sys.stdin.readline

# 한 번 getter, setter를 활용한 class로 이 문제를 해결해봤습니다.

class Rect() :
    def __init__(self, width=0, height=0):
        self.width = width
        self.height = height
    
    # 이것은 getter입니다.
    def getWidth(self) :
        return self.width
    def getHeight(self) :
        return self.height
    
    # 이것은 setter입니다.
    def setWidth(self, w) :
        self.width = w
    def setHeight(self, h) :
        self.height = h

    def area(self) :
        return self.width * self.height

L:list = [Rect() for _ in range(4)]

for i in range(4) :
    w, h = map(int, input().split())
    L[i].setWidth(w)
    L[i].setHeight(h)

left = Rect(L[0].getWidth() + L[1].getWidth(), L[0].getHeight() + L[1].getHeight())
right = Rect(L[2].getWidth() + L[3].getWidth(), L[2].getHeight() + L[3].getHeight())

left_area = left.area()
right_area = right.area()

if left_area > right_area :
    print("Right Small")
elif left_area < right_area :
    print("Left Small")
else :
    print("Same")