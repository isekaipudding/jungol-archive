# 링크 : https://jungol.co.kr/problem/2415
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())
A:list = list(map(int, input().split()))

index:int = A.index(-1)

target:int = min(max(3, index), N - 1)

value:int = 0

if index == target:
    value = A[target - 1] + A[target - 2] + A[target - 3]
elif index == target - 1:
    value = A[target] - A[target - 2] - A[target - 3]
elif index == target - 2:
    value = A[target] - A[target - 1] - A[target - 3]
elif index == target - 3:
    value = A[target] - A[target - 1] - A[target - 2]

A[index] = value

result:int = -1

if value > 0:
    status:bool = True
    
    for j in range(3, N):
        if A[j] != A[j - 1] + A[j - 2] + A[j - 3]:
            status = False
            break
            
    if status:
        result = value

print(result)