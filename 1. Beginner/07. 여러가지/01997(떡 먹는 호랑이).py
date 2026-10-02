# 링크 : https://jungol.co.kr/problem/1997
import sys

input = sys.stdin.readline

D, K = map(int, input().split())

dp1:list = [0 for _ in range(D + 1)]
dp2:list = [0 for _ in range(D + 1)]

# 초기식 1
dp1[0], dp1[1] = 0, 1

# 점화식 1
for i in range(2, D + 1, 1) :
    dp1[i] = dp1[i-1] + dp1[i-2]

# 초기식 2
dp2[0], dp2[1] = 1, 0

# 점화식 2
for i in range(2, D + 1, 1) :
    dp2[i] = dp2[i-1] + dp2[i-2]

coff_A, coff_B = dp1[D], dp2[D]

for A in range(1, K, 1) :
    if (K - coff_A * A) % coff_B :
        continue
    else :
        B:int = (K - coff_A * A) // coff_B
        print(A) # 1번째 날
        print(A + B) # 2번째 날
        break