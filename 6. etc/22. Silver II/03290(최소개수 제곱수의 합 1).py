# 링크 : https://jungol.co.kr/problem/3290
import sys

read = sys.stdin.read
write = sys.stdout.write

LIMIT = 1000000

dp = [0] * (LIMIT + 1)

# 1단계: 1개의 제곱수
for i in range(1, 1001, 1):
    dp[i * i] = 1

# 2단계: 2개의 제곱수
for i in range(1, 1001, 1):
    sq_i = i * i
    for j in range(i, 1001, 1):
        total = sq_i + j * j
        if total > LIMIT:
            break
        if not dp[total]:
            dp[total] = 2


def get_min_squares(n:int) -> int:
    if dp[n]:
        return dp[n]

    # 3단계: n - j^2의 필요 제곱수 개수가 1 또는 2인지 탐색
    for j in range(1, 1001):
        sq = j * j
        if sq >= n:
            break
        if 1 <= dp[n - sq] <= 2:
            dp[n] = 3
            return 3

    dp[n] = 4
    return 4

tokens:list = list(map(int, read().split()))

T:int = tokens[0]
output = [0] * T

for index in range(T):
    N:int = tokens[index + 1]
    output[index] = str(get_min_squares(N))

write("\n".join(output) + "\n")