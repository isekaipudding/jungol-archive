# 링크 : https://jungol.co.kr/problem/1311
import sys
from collections import Counter

input = sys.stdin.readline


L:list = []

for _ in range(5):
    color, number = map(str, input().split())
    L.append((color, int(number)))

S1:set = set()

for i in range(5):
    S1.add(L[i][0])

result:int = 0

# 만약 모든 카드들의 색깔이 같다면
if len(S1) == 1:
    numbers:list = [number for _, number in L]
    numbers.sort()
    status:bool = True
    for i in range(1, 5, 1):
        if numbers[i-1] + 1 != numbers[i]:
            status = False
            break
    # 1번 조건
    if status:
        result = 900 + max(numbers)
    # 4번 조건
    else:
        result = 600 + max(numbers)
else:
    numbers:list = [number for _, number in L]
    # 9번 조건
    result = 100 + max(numbers)
    
    numbers.sort()
    D:dict = dict(Counter(numbers))
    V:list = list(D.values())
    V.sort()
    
    reverse_D:dict = dict()
    for key, value in D.items():
        if value not in reverse_D:
            reverse_D[value] = [key]
        else:
            reverse_D[value].append(key)
    
    # 2번 조건
    if V == [1, 4]:
        result = 800 + reverse_D[4][0]
    # 3번 조건
    if V == [2, 3]:
        result = 700 + 10 * reverse_D[3][0] + reverse_D[2][0]
    # 5번 조건
    if V == [1, 1, 1, 1, 1]:
        status:bool = True
        for i in range(1, 5, 1):
            if numbers[i-1] + 1 != numbers[i]:
                status = False
                break
        if status:
            result = 500 + max(numbers)
    # 6번 조건
    if V == [1, 1, 3]:
        result = 400 + reverse_D[3][0]
    # 7번 조건
    if V == [1, 2, 2]:
        reverse_D[2].sort()
        result = 300 + 10 * reverse_D[2][1] + reverse_D[2][0]
    # 8번 조건
    if V == [1, 1, 1, 2]:
        result = 200 + reverse_D[2][0]

print(result)