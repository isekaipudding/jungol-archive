# 링크 : https://jungol.co.kr/problem/8586
import sys

input = sys.stdin.readline

# Array 자료형을 Python의 class로 구현합니다.

class Array():
    def __init__(self, a=0, b=0, c=0, d=0, e=0):
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e

    def getTuple(self):
        return (self.a, self.b, self.c, self.d, self.e)
    
    def setTuple(self, a, b, c, d, e):        
        self.a = a
        self.b = b
        self.c = c
        self.d = d
        self.e = e
    
    def changeForm(self):
        self.b = -self.b
        self.d = -self.d

N:int = int(input().rstrip())

L1:list = [Array() for _ in range(N)]
for i in range(N):
    a, b, c, d, e = map(int, input().split())
    L1[i].setTuple(a, b, c, d, e)
    L1[i].changeForm()

L2:list = [None for _ in range(N)]
for i in range(N):
    L2[i] = L1[i].getTuple()

L2.sort(key=lambda x: (x[0], x[1], x[2], x[3], x[4]))

for i in range(N):
    a, b, c, d, e = L2[i][0], L2[i][1], L2[i][2], L2[i][3], L2[i][4]
    L1[i].setTuple(a, b, c, d, e)
    L1[i].changeForm()
    L2[i] = L1[i].getTuple()

for i in range(N):
    print(*L2[i])