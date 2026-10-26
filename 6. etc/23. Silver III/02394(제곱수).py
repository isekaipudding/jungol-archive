# 링크 : https://jungol.co.kr/problem/2394
import sys

input = sys.stdin.readline

x, y, k = map(int, input().split())

# 1. 특수 케이스 처리 (0 또는 1)
if x == 0:
    print(0 if k == 0 else -1)
    sys.exit(0)

if y == 0 or x == 1:
    print(1 if k == 0 else -1)
    sys.exit(0)

# 2. x >= 2일 때 자릿수 존재 여부 검사
# k <= 4 이므로 10^k <= 10000 이며, 2^14 = 16384 > 10000
if y < 14 and (x ** y) < (10 ** k):
    print(-1)
    sys.exit(0)

# 3. 모듈러 거듭제곱을 이용한 k번째 자릿수 추출
mod = 10 ** (k + 1)
number = pow(x, y, mod)
result = number // (10 ** k)

print(result)