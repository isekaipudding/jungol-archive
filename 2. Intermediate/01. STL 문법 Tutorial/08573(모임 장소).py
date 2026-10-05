# 링크 : https://jungol.co.kr/problem/8573
import sys

input = sys.stdin.readline

N:int = int(input().rstrip())
L:list = list(map(int, input().split()))

L.sort()

# 절대 오차 |x-a|들의 합이 최소가 될려면 a는 중앙값이 되어야 합니다.
if N & 1 :
    print(L[N // 2])
else :
    a, b = L[(N // 2) - 1], L[N // 2]
    if a != b :
        print(a, b)
    else :
        print(a)