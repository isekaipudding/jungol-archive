# 링크 : https://jungol.co.kr/problem/5170
import sys
from collections import Counter

input = sys.stdin.readline

# 이 문제는 매개 변수 탐색이 아닌 그리디 알고리즘으로 더 빠르게 해결할 수 있습니다.

N, M = map(int, input().split())
trees:list = list(map(int, input().split()))

tree_counts = Counter(trees)

unique_heights:list = sorted(tree_counts.keys(), reverse=True)
unique_heights.append(0)

trees_to_cut:int = 0

for i in range(len(unique_heights) - 1):
    current_height, next_height = unique_heights[i], unique_heights[i+1]
    
    trees_to_cut += tree_counts[current_height]
    
    obtainable = (current_height - next_height) * trees_to_cut
    
    if obtainable < M:
        M -= obtainable
    else:
        cut_down = (M + trees_to_cut - 1) // trees_to_cut
        print(current_height - cut_down)
        sys.exit(0)