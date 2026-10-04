# 링크 : https://jungol.co.kr/problem/1407
import sys

input = sys.stdin.readline

def dfs(CARDS, size):
    if size <= 0:
        return 1
    
    a:int = 0
    b:int = 0
    
    one_digit = CARDS[-1]
    if 1 <= int(one_digit) <= 9:
        a = dfs(CARDS[0:size - 1:1], size - 1)
    
    if size >= 2:
        two_digit = CARDS[size - 2:size:1]
        if 10 <= int(two_digit) <= 34:
            b = dfs(CARDS[0:size - 2:1], size - 2)
    
    return a + b

cards:str = input().rstrip()

result:int = dfs(cards, len(cards))

print(result)