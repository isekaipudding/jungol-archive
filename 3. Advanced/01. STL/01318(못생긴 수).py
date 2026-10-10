# 링크 : https://jungol.co.kr/problem/1318
import sys
import math

input = sys.stdin.readline
log = math.log

# 런타임 전처리
log2 = log(2)
log3 = log(3)
log5 = log(5)

ugly_numbers:list = []

# 브루트 포스 알고리즘으로 31 * 20 * 14 = 8680개의 못생긴 수들을 모두 다 넣습니다.
# a <= floor(9 * log2(10)) -> 29
# b <= floor(9 * log3(10)) -> 18
# c <= floor(9 * log5(10)) -> 12
# 넉넉하게 각각 최대 범위를 2씩 증가시킵니다.
# 추가로 10^9 기준으로 하는 이유는 1500번째 못생긴 수는 대략 10^9 이하입니다.
for a in range(31):
    for b in range(20):
        for c in range(14):
            log_value = a * log2 + b * log3 + c * log5
            ugly_numbers.append((log_value, a, b, c))

# log 값을 기준으로 오름차순을 진행합니다.
ugly_numbers.sort(key=lambda x: x[0])

L:list = []
for i in range(min(1500, len(ugly_numbers))):
    _, a, b, c = ugly_numbers[i]
    
    # 10의 지수 추출
    e = min(a, c)
    
    base = (2 ** (a - e)) * (3 ** b) * (5 ** (c - e))
    
    L.append(str(base) + "0" * e)

# 입력부
while True:
    N:int = int(input().rstrip())
    if not N:
        break
    print(L[N - 1])