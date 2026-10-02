# 링크 : https://jungol.co.kr/problem/1856
import sys

input = sys.stdin.readline

N, M = map(int, input().split())

count:int = 0
    
for i in range(N) :
    count += 1
    if i & 1 :
        for j in range(M, 0, -1) :
            print(i * M + j, end="", flush=True)
            if count != N * M :
                print(" ", end="", flush=True)
    else :
        for j in range(1, M + 1, 1) :
            print(i * M + j, end="", flush=True)
            if count != N * M :
                print(" ", end="", flush=True)
    print()