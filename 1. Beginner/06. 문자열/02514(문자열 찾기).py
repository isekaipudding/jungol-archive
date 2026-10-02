# 링크 : https://jungol.co.kr/problem/2514
import sys

input = sys.stdin.readline

K:str = input().rstrip()
size:int = len(K)

# 예외 처리
if size < 3 :
    print(0)
    print(0)
    sys.exit(0)

KOI, IOI = 0, 0
for i in range(size - 2) :
    TEMP:str = K[i:i+3:1]
    if TEMP == "KOI" :
        KOI += 1
    if TEMP == "IOI" :
        IOI += 1

print(KOI)
print(IOI)