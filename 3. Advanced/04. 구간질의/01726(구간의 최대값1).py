# 링크 : https://jungol.co.kr/problem/1726

import sys
import math

input = sys.stdin.readline

# 세그먼트 트리 만들기
def build():
    # 리스트를 세그먼트 트리에 저장하기
    for index in range(size, size + N, 1):
        SegmentTree[index] = L[index - size]
    
    # 트리 dp(바텀 업 방식)
    for index in range(size - 1, 0, -1):
        SegmentTree[index] = max(SegmentTree[index << 1], SegmentTree[index << 1 | 1])

# 바텀 업 방식의 쿼리 실행 함수
def query(left, right):
    # 1. 0-based 인덱스로 들어온 값을 실제 트리 리프 노드 인덱스로 변환
    left += size
    right += size
    
    result = None
    
    # 두 포인터가 교차할 때까지 (루트 방향으로 올라가며) 반복
    # 원래 이 부분은 재귀 + 분할 정복으로 해야 하는데
    # 탑-다운 -> 바텀 업으로 바뀌엇 두 포인터 알고리즘으로 해결됩니다.
    while left <= right:
        
        # 2. left가 홀수 (오른쪽 자식)일 때
        if left & 1: 
            if SegmentTree[left] is not None:
                if result is None or SegmentTree[left] > result:
                    result = SegmentTree[left]
            left += 1 # 현재 값 채택 후 짝수(왼쪽 자식) 위치로 이동
            
        # 3. right가 짝수 (왼쪽 자식)일 때
        if not right & 1: # (right % 2 == 0)
            if SegmentTree[right] is not None:
                if result is None or SegmentTree[right] > result:
                    result = SegmentTree[right]
            right -= 1 # 현재 값 채택 후 홀수(오른쪽 자식) 위치로 이동
            
        # 4. 부모 노드로 한 칸 점프 (비트 우측 시프트)
        left >>= 1
        right >>= 1
        
    return result

N, Q = map(int, input().split())
L:list = []

for _ in range(N):
    L.append(int(input().rstrip()))

bits:int = int(
    math.ceil(
        math.log2(N)
    )
)
size:int = 1 << bits
SegmentTree:list = [0 for _ in range(2 * size)]

build()

for _ in range(Q):
    L, R = map(int, input().split())
    result:int = query(L - 1, R - 1)
    print(result)