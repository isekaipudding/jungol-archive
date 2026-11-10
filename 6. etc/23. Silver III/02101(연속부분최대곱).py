# 링크 : https://jungol.co.kr/problem/2101
import sys
from decimal import Decimal, ROUND_HALF_UP

input = sys.stdin.readline

N:int = int(input().rstrip())
dp:list = [Decimal("0.0")] * N

for i in range(N):
    dp[i] = Decimal(input().rstrip())

# 점화식
for i in range(1, N, 1):
    if dp[i - 1] >= Decimal("1.0"):
        dp[i] *= dp[i - 1]

result:Decimal = max(dp)

print(result.quantize(Decimal("0.000"), rounding=ROUND_HALF_UP))