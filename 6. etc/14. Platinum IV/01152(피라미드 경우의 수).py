# 링크 : https://jungol.co.kr/problem/1152
import sys

input = sys.stdin.readline

MOD = 1_000_000_007

N, T = map(int, input().split())

# 예외 처리 1
if N > 20:
    print(0)
    sys.exit(0)

# 예외 처리 2
if (1 << (N - 1)) > T:
    print(0)
    sys.exit(0)

fact = [0] * N

# 초기식 1
fact[0] = 1

# 점화식 1
for i in range(1, N, 1):
    fact[i] = i * fact[i - 1]

coins:list = [0] * N

# 동전은 (N-1)와 k의 이항 계수로 이루어져 있습니다.
for k in range(N):
    coins[k] = fact[N - 1] // fact[k] // fact[N - 1 - k]
    
target:int = T - 2 ** (N - 1)

dp:list = [0] * (target + 1)

# 초기식 2
dp[0] = 1

# 점화식 2
for coin in coins:
    for i in range(coin, target + 1, 1):
        dp[i] = (dp[i] + dp[i - coin]) % MOD

print(dp[target])