# 링크 : https://jungol.co.kr/problem/2567
import sys

input = sys.stdin.readline

D:dict = dict()
S:set = set()

N, P = map(int, input().split())

D[N] = 0
S.add(N)

current_count:int = 0
current_value:int = N

result:int = 0
while True :
    current_count += 1
    TEMP = (current_value * N) % P
    if TEMP in S :
        result = current_count - D[TEMP]
        break
    else :
        D[TEMP] = current_count
        S.add(TEMP)
        current_value = TEMP

print(result)