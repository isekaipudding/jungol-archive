# 링크 : https://jungol.co.kr/problem/1560
import sys
import math

input = sys.stdin.readline

MAX_N = 10000
LIMIT = math.isqrt(MAX_N)

counts:list = [0 for _ in range(MAX_N + 1)]

# 유클리드 공식을 사용해서 counts를 계산합니다.
for m in range(2, LIMIT + 1):
    for n in range(1, m):
        # 조건 1 -> 홀짝이 다름
        # 조건 2 -> 서로소
        if (m + n) % 2 == 1 and math.gcd(m, n) == 1:
            z = m * m + n * n
            
            # 원시 피타고라스 쌍의 빗변이 MAX_N을 넘으면 패스
            if z <= MAX_N:
                # 해당 원시 쌍의 배수들도 모두 직각삼각형 생성 가능
                k = 1
                while z * k <= MAX_N:
                    counts[z * k] += 1
                    k += 1

prefix:list = [0 for _ in range(MAX_N + 1)]
for i in range(1, MAX_N + 1):
    prefix[i] = prefix[i - 1] + counts[i]

while True:
    N:int = int(input().rstrip())
    
    if N == 0:
        break
        
    if not (1 <= N <= 10000):
        print("입력에러")
        continue
        
    print(prefix[N])