# 링크 : https://jungol.co.kr/problem/1804
"""
관리자에 의해 정해진 티어 : 플레티넘 5티어
실제 난이도 : 다이아 5티어 ~ 다이아 4티어
여기서는 다이아 5티어 폴더에 저장합니다.
"""
import sys
import math

input = sys.stdin.readline

# 이 문제는 뫼비우스 함수 공식을 안 사용하고 위키백과 등을 찾아서 스스로 해결한 문제입니다.

# lim x->+inf Q(x) / x = 6 / pi^2이므로
# x = 1_000_000_000일 때 Q(x) = 1_000_000_000 * pi^2 / 6 = 1_644_934_067이 됩니다.
# 안전하게 1_700_000_000으로 하겠습니다.
LIMIT = 1_700_000_000

def eratosthenes_sieve(n:int) -> list :
    if n < 2 :
        return []
    
    is_prime:list = [True] * (n + 1)
    
    is_prime[0], is_prime[1] = False, False
    
    for i in range(4, n + 1, 2) :
        is_prime[i] = False
        
    for i in range(3, int(math.sqrt(n)) + 1, 2) :
        if is_prime[i] :
            for j in range(i * i, n + 1, 2 * i) :
                is_prime[j] = False
                
    return [index for index, value in enumerate(is_prime) if value]

# 런타임 전처리 과정
primes:list = eratosthenes_sieve(int(math.sqrt(LIMIT)))
size:int = len(primes)

# x -> Q(x)인 경우 Q(x)를 입력으로 하여 Q(x) 이하의 square_free 수들의 개수를 구해주는 함수입니다.
# Q(x) = 19이면 13, Q(x) = 20이면 13, Q(x) = 21이면 14로 출력하게 됩니다.
def dfs(depth:int, current:int, index:int, Q_x:int) -> None :
    global result
    # IndexError 방지
    if index >= size :
        return
    for i in range(index, size, 1) :
        # 우선 최근 값에 소수 제곱을 곱해줍니다.
        TEMP:int = current * primes[i] * primes[i]
        # 만약 범위를 초과하면 백트래킹 해서 불필요한 탐색을 중지합니다.
        if TEMP > Q_x :
            break
        # if-else문에 있는 수학적 원리가 바로 포함 배제의 원리
        if depth & 1 :
            result += Q_x // TEMP
        else :
            result -= Q_x // TEMP
        dfs(depth + 1, TEMP, i + 1, Q_x)
    return

def binary_search(target:int) -> int :
    global result
    # 범위는 K 이상 1.7K 이하로 합니다.(1.7배까지만 해도 되는 이유는 LIMIT 부분을 확인해주세요.)
    lo, hi = target, target * 17 // 10
    
    while lo <= hi :
        mid:int = (lo + hi) // 2
        result = mid
        dfs(0, 1, 0, mid)
        # 만약 result가 K보다 크면 당연히 hi = mid - 1로 조정해야죠.
        # 그런데 Q(x) = 23, 24, 25인 경우 모두 x = 16이 나옵니다.
        # 그러므로 mid = 24, 25인 경우 target과 일치하는 경우라도 hi = mid - 1로 조정합니다.
        if result >= target :
            hi = mid - 1
        # 만약 result가 K보다 작으면 당연히 lo = mid + 1로 조정해야죠.
        elif result < target :
            lo = mid + 1
    return lo # 그렇게 해서 나온 lo가 바로 K번째 제곱ㄴㄴ 수입니다.

# 이전에 이미 제곱ㄴㄴ 문제를 스스로 해결했으니 여기 코드만 고치면 됩니다.
result:int = 0
while True :
    K:int = int(input().rstrip())
    if K == 0 :
        break
    print(binary_search(K))