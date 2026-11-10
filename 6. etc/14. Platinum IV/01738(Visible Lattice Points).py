# 링크 : https://jungol.co.kr/problem/1738
import sys

input = sys.stdin.readline

LIMIT = 10000

# 오일러 피 함수 전처리
# 뫼비우스 함수의 성질을 이용하여 각 합성수를 정확히 1번만 방문
phi = [0] * (LIMIT + 1)
phi[1] = 1
primes = []
is_prime = [True] * (LIMIT + 1)

for i in range(2, LIMIT + 1):
    if is_prime[i]:
        primes.append(i)
        phi[i] = i - 1
        
    for p in primes:
        if i * p > LIMIT:
            break
        is_prime[i * p] = False
        
        # i가 p로 나누어 떨어지면 p가 i의 가장 작은 소인수임
        if i % p == 0:
            phi[i * p] = phi[i] * p
            break
        # i와 p가 서로소인 경우 (뫼비우스 함수의 승법적 성질)
        phi[i * p] = phi[i] * (p - 1)

dp:list = [0] * (LIMIT + 1)

# 초기식
dp[1] = 3

# 점화식
for i in range(2, LIMIT + 1, 1):
    dp[i] = dp[i - 1] + 2 * phi[i]

T:int = int(input().rstrip())

for _ in range(T):
    N:int = int(input().rstrip())
    print(dp[N])