# 링크 : https://jungol.co.kr/problem/8074
import sys
from collections import deque

input = sys.stdin.readline

class Data():
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
    
    def setTuple(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
    
    def getTuple(self):
        return (self.x, self.y, self.z)

Q:int = int(input().rstrip())

queue = deque()

for _ in range(Q):
    query:list = list(map(str, input().split()))
    cmd:str = query[0]
    
    if cmd == "i":
        x, y, z = int(query[1]), int(query[2]), int(query[3])
        queue.append(Data(x, y, z))
    if cmd == "o":
        if queue:
            data:Data = queue.popleft()
            x, y, z = data.getTuple()
            print(x, y, z)
        else:
            print("empty")
    if cmd == "c":
        print(len(queue))
    if cmd == "z":
        a:int = int(query[1])
        if queue:
            data:Data = queue[0]
            x, y, z = data.getTuple()
            if z == a:
                print("yes")
            else:
                print("no")
        else:
            print("no")