# 링크 : https://jungol.co.kr/problem/1262
import sys

input = sys.stdin.readline

while True:
    query:list = list(map(int, input().split()))
    n:int = query[0]

    if n == 0:
        break
    
    m:int = 0
    try:
        m = query[1]
    except:
        pass
    
    print(n * m)