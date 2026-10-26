# 링크 : https://jungol.co.kr/problem/8129
import sys

input = sys.stdin.readline

# 이거 재귀가 아닌 수학(조합론)으로 해결할 수 있겠는데요?

# 이항 계수 함수
def binomial_coefficients(n:int, k:int) :
    return fact[n] // (fact[k] * fact[n-k])

# 런타임 전처리(dp cache)
LIMIT = 10

fact:list = [1 for _ in range(LIMIT + 1)]

# 초기식
fact[0] = 1

# 점화식
for i in range(1, LIMIT + 1, 1) :
    fact[i] = fact[i-1] * i

N, K = map(int, input().split())
A:list = list(map(int, input().split()))

B:list = sorted(A)

# 불가능한 경우 1
if A != B :
    print("None")
    sys.exit(0)

# 불가능한 경우 2
if not (1 <= B[0] <= N) or not (1 <= B[-1] <= N) :
    print("None")
    sys.exit(0)

# 불가능한 경우 3
if len(set(A)) != K :
    print("None")
    sys.exit(0)

current:int = 0
result:int = 0

for i in range(K) :
    k:int = K - i
    result += binomial_coefficients(N - current, k) - binomial_coefficients((N + 1) - A[i], k)
    current = A[i]

result += 1

print(result)

"""
N = 6, K = 4

1 2 3 4 = 0 + 0 + 0 + 1 = (6C4 - 6C4) + (5C3 - 5C3) + (4C2 - 4C2) + (3C1 - 3C1) + 1
1 2 3 5 = 0 + 0 + 0 + 2 = (6C4 - 6C4) + (5C3 - 5C3) + (4C2 - 4C2) + (3C1 - 2C1) + 1
1 2 3 6 = 0 + 0 + 0 + 3 = (6C4 - 6C4) + (5C3 - 5C3) + (4C2 - 4C2) + (3C1 - 1C1) + 1
1 2 4 5 = 0 + 0 + 3 + 1 = (6C4 - 6C4) + (5C3 - 5C3) + (4C2 - 3C2) + (2C1 - 2C1) + 1
1 2 4 6 = 0 + 0 + 3 + 2 = (6C4 - 6C4) + (5C3 - 5C3) + (4C2 - 3C2) + (2C1 - 1C1) + 1
1 2 5 6 = 0 + 0 + 5 + 1 = (6C4 - 6C4) + (5C3 - 5C3) + (4C2 - 2C2) + (1C1 - 1C1) + 1
1 3 4 5 = 0 + 6 + 0 + 1 = (6C4 - 6C4) + (5C3 - 4C3) + (3C2 - 3C2) + (2C1 - 2C1) + 1
1 3 4 6 = 0 + 6 + 0 + 2 = (6C4 - 6C4) + (5C3 - 4C3) + (3C2 - 3C2) + (2C1 - 1C1) + 1
1 3 5 6 = 0 + 6 + 2 + 1 = (6C4 - 6C4) + (5C3 - 4C3) + (3C2 - 2C2) + (1C1 - 1C1) + 1
1 4 5 6 = 0 + 9 + 0 + 1 = (6C4 - 6C4) + (5C3 - 3C3) + (2C2 - 2C2) + (1C1 - 1C1) + 1
2 3 4 5 = 10 + 0 + 0 + 1 = (6C4 - 5C4) + (4C3 - 4C3) + (3C2 - 3C2) + (2C1 - 2C1) + 1
2 3 4 6 = 10 + 0 + 0 + 2 = (6C4 - 5C4) + (4C3 - 4C3) + (3C2 - 3C2) + (2C1 - 1C1) + 1
2 3 5 6 = 10 + 0 + 2 + 1 = (6C4 - 5C4) + (4C3 - 4C3) + (3C2 - 2C2) + (1C1 - 1C1) + 1
2 4 5 6 = 10 + 3 + 0 + 1 = (6C4 - 5C4) + (4C3 - 3C3) + (2C2 - 2C2) + (1C1 - 1C1) + 1
3 4 5 6 = 14 + 0 + 0 + 1 = (6C4 - 4C4) + (3C3 - 3C3) + (2C2 - 2C2) + (1C1 - 1C1) + 1
"""