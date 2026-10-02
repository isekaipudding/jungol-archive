# 링크 : https://jungol.co.kr/problem/2857
import sys

input = sys.stdin.readline

LIMIT = 5

word:list = ["" for _ in range(LIMIT)]
size:list = [0 for _ in range(LIMIT)]

for i in range(LIMIT) :
    word[i] = input().rstrip()
    size[i] = len(word[i])

MAX_SIZE =  max(size)

result:str = ""

for c in range(MAX_SIZE) :
    for r in range(LIMIT) :
        if c < size[r] :
            result += word[r][c]

print(result)