# 링크 : https://jungol.co.kr/problem/1534
import sys

input = sys.stdin.readline

A, B = map(int, input().split())

if B == 2 :
    print(bin(A)[2::])
elif B == 8 :
    print(oct(A)[2::])
elif B == 16 :
    print(hex(A)[2::].upper())