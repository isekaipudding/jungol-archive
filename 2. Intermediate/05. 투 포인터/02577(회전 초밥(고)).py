# 링크 : https://jungol.co.kr/problem/2577
import sys

input = sys.stdin.readline

N, d, k, c = map(int, input().split())

sushi:list = [0 for _ in range(N)]

for i in range(N):
    sushi[i] = int(input().rstrip())

sushi.extend(sushi[:k-1])

counts:list = [0 for _ in range(d + 1)]

counts[c] = 1
unique_count:int = 1

for i in range(k):
    if counts[sushi[i]] == 0:
        unique_count += 1
    counts[sushi[i]] += 1
    
max_sushi:int = unique_count

# 슬라이딩 윈도우
for i in range(1, N, 1):
    out_sushi = sushi[i - 1]
    counts[out_sushi] -= 1
    if counts[out_sushi] == 0:
        unique_count -= 1
        
    in_sushi = sushi[i + k - 1]
    if counts[in_sushi] == 0:
        unique_count += 1
    counts[in_sushi] += 1
    
    if unique_count > max_sushi:
        max_sushi = unique_count
        
print(max_sushi)