# 링크 : https://jungol.co.kr/problem/1274
import sys

input = sys.stdin.readline

bits:str = input().rstrip()
size:int = len(bits)

if bits[0] == "0":
    result:int = 0
    shift:int = 1
    for i in range(size - 1, 0, -1):
        result += shift * int(bits[i])
        shift <<= 1
    print(result)
if bits[0] == "1":
    result:int = 1 << size
    shift:int = 1
    for i in range(size - 1, -1, -1):
        result -= shift * int(bits[i])
        shift <<= 1
    print(-result)