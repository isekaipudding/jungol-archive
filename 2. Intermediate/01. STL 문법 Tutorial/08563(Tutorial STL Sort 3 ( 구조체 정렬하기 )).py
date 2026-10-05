# 링크 : https://jungol.co.kr/problem/8563
import sys
from decimal import Decimal

input = sys.stdin.readline

class Student():
    def __init__(self, age=0, height=Decimal("0.0")):
        self.age = age
        self.height = height
    
    def getTuple(self):
        return (self.age, self.height)
    
    def setTuple(self, age, height):
        self.age = age
        self.height = height

N:int = int(input().rstrip())
L1:list = [Student() for _ in range(N)]

for i in range(N):
    a, b = map(str, input().split())
    L1[i].setTuple(int(a), Decimal(b))

L2:list = [None for _ in range(N)]

for i in range(N):
    L2[i] = L1[i].getTuple()

L2.sort(key=lambda x: (x[0], x[1]), reverse=True)

for i in range(N):
    print(*L2[i])

print()
L2.sort(key=lambda x: (x[1], x[0]))

for i in range(N):
    print(*L2[i])