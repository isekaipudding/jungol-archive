# 링크 : https://jungol.co.kr/problem/2326
import sys
from collections import deque

input = sys.stdin.readline

N, K = map(int, input().split())

queue = deque([i for i in range(1, N+1, 1)]) # 큐 자료구조 사용

result:list = []

while len(queue) > 0 :
    queue.rotate(-(K-1)) # 테스트 케이스에서 계산 노가다를 하면 회전을 K-1번 하면 된다는 것을 알 수 있습니다.
    result.append(queue.popleft())
    
print("<"+", ".join(map(str, result))+">") # 출력 형식에 맞게 출력합니다.