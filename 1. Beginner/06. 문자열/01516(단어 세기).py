# 링크 : https://jungol.co.kr/problem/1516
import sys
from collections import Counter

input = sys.stdin.readline

while True :
    sentence:str = input().rstrip()
    if sentence == "END" :
        break
    
    D:dict = dict(
        Counter(
            list(
                map(
                    str,
                    sentence.split()
                )
            )
        )
    )
    
    keys:list = list(D.keys())
    keys.sort()
    
    for k in keys :
        v:int = D[k]
        print(f"{k} : {v}")