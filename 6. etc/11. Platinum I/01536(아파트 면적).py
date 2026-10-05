# 링크 : https://jungol.co.kr/problem/1536
import sys

input = sys.stdin.readline

# 단일 base 'a'에 대해 밀러-라빈 소수 판별을 수행합니다.
def miller_rabin(n, a):
    d = n - 1
    while d % 2 == 0:
        d //= 2
    
    x = pow(a, d, n)
    if x == 1 or x == n - 1:
        return True
    
    # d를 2배씩 늘려가며 n-1이 되는지 확인
    while d < n - 1:
        x = pow(x, 2, n)
        if x == n - 1:
            return True
        d *= 2
        
    return False

# N < 2^64 범위에서 100% 정확도를 보장하는 결정론적 소수 판별 함수
def is_prime(n):
    if n <= 1:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # 2^64 이하의 수에 대해 100% 정확도를 보장하는 12개의 소수 Base
    bases = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]
    for a in bases:
        if n == a:
            return True
        if not miller_rabin(n, a):
            return False
            
    return True

N:int = int(input().rstrip())

result:int = 0
for _ in range(N):
    p:int = int(input().rstrip())
    if is_prime(2 * p + 1):
        result += 1

print(result)

# 아래 코드에서 수동으로 1 ~ 1000까지 x + y + 2xy를 직접 찾아봤습니다.
# N = 1, 2, 3, 5, 6, 8, 9, 11, 14, ... 이들의 공통점은 2N + 1는 항상 소수(prime number)입니다.
# 그러므로 2N + 1이 소수인 경우 x + y + 2xy는 성립할 수 없습니다.
# 다르게 말하면 2N + 1이 합성수이면 x + y + 2xy는 성립합니다.
"""
LIMIT = 10000

check:list = [True for _ in range(LIMIT + 1)]

# y가 최소 1일 때 3x + 1 <= LIMIT 이므로 x의 상한선은 (LIMIT - 1) // 3
for x in range(1, (LIMIT - 1) // 3 + 1):
    # 중복 계산 방지를 위해 y는 x부터 시작
    # x + y + 2xy <= LIMIT 부등식을 y에 대해 정리하면 y <= (LIMIT - x) / (2x + 1)
    for y in range(x, (LIMIT - x) // (2 * x + 1) + 1):
        check[x + y + 2 * x * y] = False

L:list = []
for i in range(1, LIMIT + 1, 1):
    if check[i]:
        L.append(i)

for i in range(0, 1001, 1):
    if L[i] <= 1000:
        print(L[i])
    else:
        break
"""