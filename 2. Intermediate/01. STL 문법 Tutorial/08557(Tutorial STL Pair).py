# 링크 : https://jungol.co.kr/problem/8557
import sys

input = sys.stdin.readline

# Pair 자료형을 Python의 class로 구현합니다.

class Pair():
    def __init__(self, first=0, second=0):
        self.first = first
        self.second = second
    
    def getTuple(self):
        return (self.first, self.second)
    def setTuple(self, u, v):
        self.first = u
        self.second = v

N:int = int(input().rstrip())
L1:list = [Pair() for _ in range(N)]

for i in range(N):
    a, b = map(int, input().split())
    L1[i].setTuple(a, b)

L2:list = [None for _ in range(N)]
for i in range(N):
    L2[i] = L1[i].getTuple()

L2.sort(key=lambda x: (x[0], x[1]))

for a, b in L2:
    print(a * b)