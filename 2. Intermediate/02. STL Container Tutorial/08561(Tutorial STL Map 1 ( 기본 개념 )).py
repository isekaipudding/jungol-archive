# 링크 : https://jungol.co.kr/problem/8561
import sys

input = sys.stdin.readline

D:dict = dict()

index:int = 1
while True:
    name:str = input().rstrip()
    if name == "end":
        break
    
    D[name] = index
    
    index += 1

result:list = []

for name, index in D.items():
    result.append((name, index))

result.sort(key=lambda x: x[0])

size:int = len(result)
print(size)
for i in range(size):
    name, index = result[i]
    print(name, index)