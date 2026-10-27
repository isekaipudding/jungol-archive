# 링크 : https://jungol.co.kr/problem/1027
import sys

sys.setrecursionlimit(1 << 20)
input = sys.stdin.readline

def is_good(sequence:list) -> bool:
    length:int = len(sequence)
    # 비교할 부분 수열의 길이 L ==> 1부터 전체 길이의 절반까지
    for L in range(1, (length >> 1) + 1):
        if sequence[-L:] == sequence[-2 * L : -L]:
            return False
    return True

def dfs(sequence:list) -> None:
    # 길이 N에 도달한 첫 번째 수열이 사전순 최소
    if len(sequence) == N:
        print("".join(map(str, sequence)))
        sys.exit(0)

    # 사전순 최소를 위해 1 -> 2 -> 3 순서로 분기
    for digit in (1, 2, 3):
        sequence.append(digit)
        if is_good(sequence):
            dfs(sequence)
        sequence.pop() # 백트래킹 복구

N:int = int(input().rstrip())

dfs([])