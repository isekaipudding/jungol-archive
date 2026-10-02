# 링크 : https://jungol.co.kr/problem/1535
import sys

input = sys.stdin.readline

S:set = set()
result:list = []

while True :
    sentence:str = input().rstrip()
    if sentence == "END" :
        break
    
    L:list = list(map(str, sentence.split()))
    
    for word in L :
        if word not in S :
            S.add(word)
            result.append(word)
    
    print(*result)