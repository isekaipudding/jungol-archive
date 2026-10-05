# 링크 : https://jungol.co.kr/problem/10396
import sys

input = sys.stdin.readline

# 문제에서 이미 "이거 소수입니다!"라고 입력에서 보장해줘서
# 굳이 에라토스테네스의 체, 밀러-라빈 등을 안 써도 되네요.
# 아까 제출한 다른 소스 코드는 TLE가 나오니 N = 100, P_i <= 500라는 것을 이용해
# 특수한 경우의 애드혹 공식을 사용합니다.

T:int = int(input().rstrip())

for number in range(1, T + 1, 1):
    M:int = int(input().rstrip())
    
    primes:list = []
    total:int = 0
    
    for _ in range(M):
        p, n = map(int, input().split())
        primes.append((p, n))
        total += p * n
    
    lo, hi = max(0, total - 30000), total
    
    result:int = 0
    
    for target_product in range(hi, lo - 1, -1):
        temp = target_product
        sum_of_factors = 0
        status = True

        for prime, max_count in primes:
            if temp % prime != 0:
                continue
                
            used_count = 0
            # 여기가 무한 루프 빠지는 구간이네요.
            # 그러니 temp == 0이 될 때 빠져나갑니다.
            while temp % prime == 0 and temp:
                used_count += 1
                temp //= prime
                sum_of_factors += prime
                
            # 덱에 가진 해당 소수 카드의 장수보다 더 많이 필요하다면 실패
            if used_count > max_count:
                status = False
                break
        if status and temp == 1 and sum_of_factors == total - target_product:
            result = target_product
            break
    
    print(f"Case #{number}: {result}")