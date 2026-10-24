# 링크 : https://jungol.co.kr/problem/11044
import sys

input = sys.stdin.readline

# 에디토리얼 : https://en.wikipedia.org/wiki/Farey_sequence
# C++는 그냥 간단한 O(K) 수준으로 끝나는데
# Python은 O(log K)가 강요되네요.

# 뫼비우스 함수 + 오일러 피 함수
def get_mu_phi(n):
    mu = [0] * (n + 1)
    phi = [0] * (n + 1)
    primes = []
    is_prime = [True] * (n + 1)
    
    mu[1] = 1
    phi[1] = 1
    
    for i in range(2, n + 1):
        if is_prime[i]:
            primes.append(i)
            mu[i] = -1
            phi[i] = i - 1
        for p in primes:
            if i * p > n:
                break
            is_prime[i * p] = False
            if i % p == 0:
                mu[i * p] = 0
                phi[i * p] = phi[i] * p
                break
            else:
                mu[i * p] = -mu[i]
                phi[i * p] = phi[i] * (p - 1)
    return mu, phi

# 실수 x 이하의 기약 분수 개수를 뫼비우스 반전 공식으로 카운트
# 이 때 시간 복잡도는 O(N log N)
def count_leq_real(x):
    count = 0
    for i in range(1, n + 1):
        if mu[i] != 0:
            s = 0
            limit = n // i
            for j in range(1, limit + 1):
                s += int(j * x)
            count += mu[i] * s
    return count + 1
    
# 부동소수점 오차 검증을 위한 정수 분수 카운트
def count_leq_exact(num, den):
    count = 0
    for i in range(1, n + 1):
        if mu[i] != 0:
            s = 0
            limit = n // i
            for j in range(1, limit + 1):
                s += (j * num) // den
            count += mu[i] * s
    return count + 1

# 여기서 실수 근사값을 구합니다.
def binary_search():
    low, high = 0.0, 1.0
    for _ in range(45):
        mid = (low + high) / 2.0
        if count_leq_real(mid) >= k:
            high = mid
        else:
            low = mid
    return high

n, k = map(int, input().split())

if k == 1:
    print("0 1")
    sys.exit(0)
    
mu, phi = get_mu_phi(n)

# 1. 오일러 파이 함수를 이용한 전체 기약 분수 개수(길이) 계산
total = 1
for i in range(1, n + 1):
    total += phi[i]
    
if k == total:
    print("1 1")
    sys.exit(0)
    
# 2. 좌우 대칭(Symmetry) 최적화: k가 절반을 넘어가면 반전
# 이렇게 해야 상수 계수가 약 절반 정도 줄어듭니다.
mirror = False
if k > total // 2:
    k = total - k + 1
    mirror = True

# 3. 실수 범위 [0.0, 1.0]에서 이분 탐색 (45번 반복으로 O(log K) 탐색 완료)
value = binary_search()
        
# 4. 스턴-브로코 트리(Stern-Brocot Tree)를 타고 내려가며 실수(high)를 분수로 복원
# 이때 매번 count 연산을 하지 않고 O(1) 실수 비교만 하므로 순식간에 끝납니다.
L_num, L_den = 0, 1
R_num, R_den = 1, 1

while L_den + R_den <= n:
    M_num = L_num + R_num
    M_den = L_den + R_den
    
    # 찾은 실수 근사값(value)을 이용해 방향 결정
    if value < M_num / M_den:
        R_num, R_den = M_num, M_den
    else:
        L_num, L_den = M_num, M_den
        
# 스턴-브로코 트리가 멈춘 곳의 L과 R 중 정답이 무조건 있습니다.
# float 연산이 아닌 integer 연산으로 부동소수점 오차 방지
if count_leq_exact(L_num, L_den) == k:
    result_num, result_den = L_num, L_den
else:
    result_num, result_den = R_num, R_den
    
# 좌우 대칭이 적용된 경우 분자 반전 (1 - a/b = (b - a)/b)
if mirror:
    result_num = result_den - result_num
    
print(f"{result_num} {result_den}")