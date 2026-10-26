# 링크 : https://jungol.co.kr/problem/4642
import sys

input = sys.stdin.readline

class Student():
    def __init__(self, name="", score=0):
        self.name = name
        self.score = score
    
    def getTuple(self):
        return (self.name, self.score)

    def setTuple(self, name, score):
        self.name = name
        self.score = score

N:int = int(input().rstrip())
students:list = [Student() for _ in range(N)]

for i in range(N):
    name, score = map(str, input().split())
    students[i].setTuple(name, int(score))

L:list = [None for _ in range(N)]

for i in range(N):
    L[i] = students[i].getTuple()

L.sort(key=lambda x: (-x[1], x[0]))

for name, score in L:
    print(name, score)