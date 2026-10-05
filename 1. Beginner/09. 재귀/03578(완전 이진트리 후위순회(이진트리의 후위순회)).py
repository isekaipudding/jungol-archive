# 링크 : https://jungol.co.kr/problem/3578
import sys
import math

input = sys.stdin.readline

def dfs(index:int):
    if index > size:
        return
    
    dfs(index << 1)
    dfs(index << 1 | 1)
    result.append(BST[index])

size:int = int(input().rstrip())
N:int = int(
    math.ceil(
        math.log2(size + 1)
    )
)

# 완전 이진 트리는 리스트로 구현할 수 있습니다.
BST:list = [None for _ in range(1 << N)]

data:str = input().rstrip()

for i in range(1, size + 1, 1):
    BST[i] = data[i-1]

result:list = []

dfs(1)

print("".join(map(str, result)))