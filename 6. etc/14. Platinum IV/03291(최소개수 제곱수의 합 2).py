# 링크 : https://jungol.co.kr/problem/3291
"""
관리자에 의해 정해진 티어 : 골드 5티어
실제 난이도 : 플레티넘 4티어(N = 10^10) 기준, 다이아 3티어(N = 10^18 기준)
여기서는 플레티넘 4티어 폴더에 저장합니다.
"""
import sys
import math

input = sys.stdin.readline

# 라그랑주의 네 제곱수 정리 : https://en.wikipedia.org/wiki/Lagrange%27s_four-square_theorem
# 르장드르의 세 제곱수 정리 : https://en.wikipedia.org/wiki/Legendre%27s_three-square_theorem
# 페르마의 두 제곱수 정리 : https://en.wikipedia.org/wiki/Fermat%27s_theorem_on_sums_of_two_squares

def lagrange(N:int) -> int:
    # 1. 1개의 제곱수로 표현 가능한가?
    if math.isqrt(N) ** 2 == N:
        return 1
        
    # 2. 4개의 제곱수가 필요한가?(르장드르의 세 제곱수 정리)
    # 4^a(8b + 7) 꼴인지 확인
    temp = N
    while temp % 4 == 0:
        temp >>= 2
    if temp % 8 == 7:
        return 4
        
    # 3. 2개의 제곱수로 표현 가능한가?
    # N이 최대 100억이므로 isqrt(N)은 최대 10만입니다.
    # 즉, 1부터 10만까지만 반복문을 돌면서 N - i^2 가 제곱수인지 확인합니다.
    limit = math.isqrt(N)
    for i in range(1, limit + 1):
        remain = N - i * i
        # 남은 수가 완전제곱수라면 두 제곱수의 합으로 표현 가능
        if math.isqrt(remain) ** 2 == remain:
            return 2
            
    # 4. 1, 2, 4개로 안 된다면 라그랑주의 네 제곱수 정리에 의해 무조건 3개입니다.
    return 3

T:int = int(input().rstrip())
for _ in range(T):
    N:int = int(input().rstrip())
    print(lagrange(N))