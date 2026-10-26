# 링크 : https://jungol.co.kr/problem/1803
import sys

input = sys.stdin.readline

D:dict = {
    0: "0",
    1: "1",
    2: "4",
    3: "9"
}

N:int = int(input().rstrip())

# 예외 처리
if N == 0:
    print("0")
    sys.exit(0)

result:list = []

while N:
    result.append(D[N % 4])
    N //= 4

result.reverse()

print("".join(result))