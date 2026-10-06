# 링크 : https://jungol.co.kr/problem/5656
import sys
from collections import Counter

input = sys.stdin.readline

N:int = int(input().rstrip())
L:list = list(map(int, input().rstrip())) # split()이 아니라 rstrip()으로!

prefix:list = [0 for _ in range(N + 1)]

for i in range(1, N + 1, 1):
    prefix[i] = prefix[i - 1] + L[i - 1]

# prefix[i] - i 값을 저장하고 개수를 셀 Counter 객체
count_dict = Counter()
result:int = 0

for i in range(N + 1):
    # 핵심 공식: S = prefix[i] - i
    S = prefix[i] - i
    
    # 이전에 같은 S 값이 나온 적이 있다면, 
    # 그 개수만큼 새로운 구간을 만들 수 있으므로 정답에 더해줍니다.
    result += count_dict[S]
    
    # 현재 S 값의 등장 횟수를 1 증가시킵니다.
    count_dict[S] += 1

print(result)