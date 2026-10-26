# 링크 : https://jungol.co.kr/problem/17248
import sys
import math

input = sys.stdin.readline
floor = math.floor
gamma = math.lgamma
log = math.log

# 감마 함수를 써야 할 정도로 이 문제는 정말 어렵습니다.

def get_digits(n:int) -> int:
    if n <= 1:
        return 1
    return floor(gamma(n + 1) / log(10)) + 1

def binary_search():
    high = 7
    while get_digits(high) < L:
        high <<= 1
    low = high >> 1
    
    while low <= high:
        mid = (low + high) // 2
        digits = get_digits(mid)
        
        if digits == L:
            print(mid)
            return
        elif digits < L:
            low = mid + 1
        else:
            high = mid - 1

S = input().rstrip()

L = len(S)

# N <= 6 인 경우는 자릿수가 겹칠 수 있으므로 입력값 원본 문자로 직접 판별합니다.
if L == 1:
    if S == "1": print(1)
    elif S == "2": print(2)
    elif S == "6": print(3)
    sys.exit(0)
elif L == 2:
    print(4)
    sys.exit(0)
elif L == 3:
    if S == "120": print(5)
    elif S == "720": print(6)
    sys.exit(0)
    
binary_search()