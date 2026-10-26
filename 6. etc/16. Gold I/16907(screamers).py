# 링크 : https://jungol.co.kr/problem/16907
import sys

input = sys.stdin.readline

MOD = 1000000007

D, R = map(int, input().split())

R2 = R * R

current_dp:list = [0] * (R2 + 1)

# 초기식1(거리가 0인 원점 1개)
current_dp[0] = 1

# 점화식1
for current_dimension in range(1, D, 1):
    next_dp = [0] * (R2 + 1)
    
    for squared_distance in range(R2 + 1):
        if current_dp[squared_distance] == 0:
            continue
        
        # 좌표가 0인 경우(거리 제곱이 증가하지 않음, 경우의 수 1배)
        next_dp[squared_distance] = (next_dp[squared_distance] + current_dp[squared_distance]) % MOD
        
        # 좌표가 1, 2, 3... 인 경우(+와 - 양쪽 대칭이므로 경우의 수 2배)
        value = 1
        while squared_distance + value * value <= R2:
            next_squared_distance = squared_distance + value * value
            next_dp[next_squared_distance] = (next_dp[next_squared_distance] + 2 * current_dp[squared_distance]) % MOD
            value += 1
            
    current_dp = next_dp

prefix:list = [0] * (R2 + 1)

# 초기식2
prefix[0] = current_dp[0]

# 점화식2
for squared_distance in range(1, R2 + 1, 1):
    prefix[squared_distance] = (prefix[squared_distance - 1] + current_dp[squared_distance]) % MOD

total:int = 0

for value in range(1, R + 1, 1):
    total = (total + value * prefix[R2 - value * value]) % MOD

result:int = (total * 2 * D) % MOD

print(result)