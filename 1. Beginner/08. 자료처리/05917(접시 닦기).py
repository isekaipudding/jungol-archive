# 링크 : https://jungol.co.kr/problem/5917
import sys

input = sys.stdin.readline

N, T = map(int, input().split())

before_dish:list = [i for i in range(N, 0, -1)]
after_dish:list = []
finish_dry:list = []

for _ in range(T) :
    query:list = list(map(int, input().split()))
    cmd, repeat = query[0], query[1]
    
    if cmd == 1 :
        for _ in range(repeat) :
            after_dish.append(before_dish.pop())
    if cmd == 2 :
        for _ in range(repeat) :
            finish_dry.append(after_dish.pop())

while finish_dry :
    print(finish_dry.pop())