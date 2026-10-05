# 링크 : https://jungol.co.kr/problem/2581
import sys
from collections import Counter

input = sys.stdin.readline

# 이 문제는 매개 변수 탐색이 아닌 그리디 알고리즘으로 더 빠르게 해결할 수 있습니다.

N:int = int(input().rstrip())
requests:list = list(map(int, input().split()))
MAX_LIMIT:int = int(input().rstrip())

total_request:int = sum(requests)

# 예외 처리
if total_request <= MAX_LIMIT:
    print(max(requests))
    sys.exit(0)

# 이렇게 바꾸면 이전의 나무 자르기 문제와 동일하게 바뀝니다.
cut_target:int = total_request - MAX_LIMIT

request_counts = Counter(requests)
unique_requests:list = sorted(request_counts.keys(), reverse=True)
unique_requests.append(0)

items_to_cut = 0

for i in range(len(unique_requests) - 1):
        current_requests = unique_requests[i]
        next_requests = unique_requests[i+1]
        
        items_to_cut += request_counts[current_requests]

        obtainable = (current_requests - next_requests) * items_to_cut
        
        if obtainable < cut_target:
            cut_target -= obtainable
        else:
            cut_down = (cut_target + items_to_cut - 1) // items_to_cut
            print(current_requests - cut_down)
            sys.exit(0)