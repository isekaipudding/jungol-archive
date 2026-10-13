# 링크 : https://jungol.co.kr/problem/5196
import sys
from collections import defaultdict

input = sys.stdin.readline

N:int = int(input().rstrip())
L:list = list(map(int, input().split()))

# N이 2 이하인 경우 두 점은 항상 등차수열을 이룸
if N <= 2:
    print(0)
    sys.exit(0)

max_preserved = 2 # 최소 2개는 항상 유지 가능

for i in range(N):
    diff_count = defaultdict(int)
    for j in range(i + 1, N, 1):
        dx = j - i
        dy = L[j] - L[i]
        
        # 기울기(공차 d)가 정수인 경우만 유효
        if dy % dx == 0:
            d = dy // dx
            diff_count[d] += 1
            
            # 기준점 i를 포함하므로 +1
            max_preserved = max(max_preserved, diff_count[d] + 1)

print(N - max_preserved)