# 링크 : https://jungol.co.kr/problem/8591
import sys

input = sys.stdin.readline

R, C = map(int, input().split())

graph:list = []
for _ in range(R):
    graph.append(list(map(int, input().split())))

result:int = -float('inf')

for r1 in range(R):
    prefix:list = [0] * C
    
    for r2 in range(r1, R, 1):
        row = graph[r2]
        current_sum = 0
        
        for c in range(C):
            prefix[c] += row[c]
        
            if current_sum > 0:
                current_sum += prefix[c]
            else:
                current_sum = prefix[c]
            
            result = max(result, current_sum)

print(result)