# 링크 : https://jungol.co.kr/problem/7052
import sys

input = sys.stdin.readline

R, S, a, b = map(int, input().split())

graph:list = []

for _ in range(R):
    graph.append(list(map(int, input().split())))

if R > S:
    graph = [[graph[r][c] for r in range(R)] for c in range(S)]
    R, S = S, R

MIN, MAX = min(a, b), max(a, b)
min_possible = MAX - MIN
result = float('inf')

targets = [MIN] if MIN == MAX else [MIN, MAX]

for r1 in range(R):
    col_prefix = [0] * S
    for r2 in range(r1, R):
        row_r2 = graph[r2]
        for c in range(S):
            col_prefix[c] += row_r2[c]
            
        # 각 목표값 T (L과 U)에 대해 투 포인터 실행
        for T in targets:
            left = 0
            current = 0
            for right in range(S):
                current += col_prefix[right]
                
                # current >= T인 지점들을 거치며 T 이상 최솟값 탐색
                while left <= right and current >= T:
                    value = abs(current - a) + abs(current - b)
                    if value < result:
                        result = value
                        if result == min_possible:
                            print(result)
                            sys.exit(0)
                    current -= col_prefix[left]
                    left += 1
                    
                # 루프 종료 후 current < T인 상태에서 T 미만 최댓값 탐색(단, 빈 구간 제외)
                if left <= right:
                    value = abs(current - a) + abs(current - b)
                    if value < result:
                        result = value
                        if result == min_possible:
                            print(result)
                            sys.exit(0)

print(result)