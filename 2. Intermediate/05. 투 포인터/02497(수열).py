# 링크 : https://jungol.co.kr/problem/2497
import sys

input = sys.stdin.readline

N, K = map(int, input().split())
L:list = list(map(int, input().split()))

prefix:list = [0 for _ in range(N + 1)]

# 초기식
prefix[0] = 0

# 점화식
for i in range(1, N + 1, 1) :
    prefix[i] = prefix[i - 1] + L[i - 1]

start, end = 0, K

# 투 포인터 사용
result:int = -100 * K
while end <= N :
    result = max(result, prefix[end] - prefix[start])
    # 이 문제는 슬라이딩 윈도우 알고리즘을 사용하면 됩니다.
    start += 1
    end += 1

print(result)