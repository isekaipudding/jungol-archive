# 링크 : https://jungol.co.kr/problem/2858
import sys

input = sys.stdin.readline

pipe:str = input().rstrip().replace("()", "1")

stack:list = []

result:int = 0
for stick in pipe :
    if stack :
        if stick == ")" :
            TEMP_COUNT = 0
            while stack :
                TEMP_STICK = stack.pop()
                if TEMP_STICK == "(" :
                    result += TEMP_COUNT + 1
                    if stack :
                        stack.append(str(TEMP_COUNT))
                    break
                else :
                    TEMP_COUNT += int(TEMP_STICK)
        else :
            stack.append(stick)
    elif not stack and stick == "(" :
        stack.append(stick)

print(result)