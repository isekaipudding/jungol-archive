# 링크 : https://jungol.co.kr/problem/1161
import sys

input = sys.stdin.readline

def dfs(depth:int, a:int, b:int, c:int) -> None :
    if depth == 0 :
        return
    
    dfs(depth - 1, a, c, b)
    print(f"{depth} : {a} -> {c}")
    dfs(depth - 1, b, a, c)

N:int = int(input().rstrip())

dfs(N, 1, 2, 3)

"""
N번 원판 위에 N-1번 원판이 있다고 가정합니다.
둘 다 현재 a 위치에 있습니다.
만약 N번 원판을 c 위치에 배치하고 싶다면
반드시 N-1번 원판을 b 위치에 놔두고
그 다음 N번 원판을 c 위치에 배치를 해서
N-1번 원판을 c 위치에 두면 됩니다.
이것을 식으로 표현하면 다음과 같습니다.

N-1 : a -> b
N : a -> c
N-1 : b -> c
이 때 반드시 이 순서대로 3단계를 진행해야 합니다.
"""