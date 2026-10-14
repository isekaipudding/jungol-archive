# 링크 : https://jungol.co.kr/problem/3516
import sys

input = sys.stdin.readline

D1, D2 = map(int, input().split())

# 오일러 피 함수 전처리
# 뫼비우스 함수의 성질을 이용하여 각 합성수를 정확히 1번만 방문
phi = [0] * (D2 + 1)
phi[1] = 1
primes = []
is_prime = [True] * (D2 + 1)

for i in range(2, D2 + 1):
    if is_prime[i]:
        primes.append(i)
        phi[i] = i - 1
        
    for p in primes:
        if i * p > D2:
            break
        is_prime[i * p] = False
        
        # i가 p로 나누어 떨어지면 p가 i의 가장 작은 소인수임
        if i % p == 0:
            phi[i * p] = phi[i] * p
            break
        # i와 p가 서로소인 경우 (뫼비우스 함수의 승법적 성질)
        phi[i * p] = phi[i] * (p - 1)

# 비둘기집 원리를 이용한 구간 최적화
total_seats = 0
threshold = D2 - D1 + 1
M = D1 - 1

for b in range(1, D2 + 1):
    # 검사 없이 즉시 통과
    if b <= threshold or b >= D1:
        total_seats += phi[b]
    # 틈새 구간 정밀 검사
    elif (D2 // b) > (M // b):
        total_seats += phi[b]

print(total_seats)