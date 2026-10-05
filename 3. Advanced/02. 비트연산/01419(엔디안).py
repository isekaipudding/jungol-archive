# 링크 : https://jungol.co.kr/problem/1419
import sys

input = sys.stdin.readline

HEX_TO_INT:dict = {
    "0": 0,
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "a": 10,
    "b": 11,
    "c": 12,
    "d": 13,
    "e": 14,
    "f": 15,
}

N:int = int(input().rstrip())
H:str = hex(N)[2::]
size:int = len(H)

H = "0" * (8 - size) + H

H = H[6:8:1] + H[4:6:1] + H[2:4:1] + H[0:2:1]

result:int = 0
shift:int = 1

for i in range(7, -1, -1):
    result += shift * HEX_TO_INT[H[i]]
    shift <<= 4

print(result)