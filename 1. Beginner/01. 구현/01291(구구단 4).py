# 링크 : https://jungol.co.kr/problem/1291
import sys

input = sys.stdin.readline

while True :
    A, B = map(int, input().split())
    
    if A < 2 or A > 9 :
        print("INPUT ERROR!")
        continue
    if B < 2 or B > 9 :
        print("INPUT ERROR!")
        continue

    start, end, step = A, B, 0

    if A <= B :
        end += 1
        step += 1
    else :
        end -= 1
        step -= 1
        
    for j in range(1, 10, 1) :
        for i in range(start, end, step) :
            print(f"{i} * {j} = {i * j:>2}", end="", flush=True)
            if i + step != end :
                print("   ", end="", flush=True)
        print()
        
    break